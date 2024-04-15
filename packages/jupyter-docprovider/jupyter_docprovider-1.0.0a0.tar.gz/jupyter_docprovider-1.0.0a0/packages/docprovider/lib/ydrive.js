// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { PageConfig, URLExt } from '@jupyterlab/coreutils';
import { Drive } from '@jupyterlab/services';
import { WebSocketProvider } from './yprovider';
const DISABLE_RTC = PageConfig.getOption('disableRTC') === 'true' ? true : false;
/**
 * The url for the default drive service.
 */
const DOCUMENT_PROVIDER_URL = 'api/collaboration/room';
/**
 * A Collaborative implementation for an `IDrive`, talking to the
 * server using the Jupyter REST API and a WebSocket connection.
 */
export class YDrive extends Drive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(user, translator) {
        super({ name: 'RTC' });
        this._onCreate = (options, sharedModel) => {
            if (typeof options.format !== 'string') {
                return;
            }
            try {
                const provider = new WebSocketProvider({
                    url: URLExt.join(this.serverSettings.wsUrl, DOCUMENT_PROVIDER_URL),
                    path: options.path,
                    format: options.format,
                    contentType: options.contentType,
                    model: sharedModel,
                    user: this._user,
                    translator: this._trans
                });
                const key = `${options.format}:${options.contentType}:${options.path}`;
                this._providers.set(key, provider);
                sharedModel.disposed.connect(() => {
                    const provider = this._providers.get(key);
                    if (provider) {
                        provider.dispose();
                        this._providers.delete(key);
                    }
                });
            }
            catch (error) {
                // Falling back to the contents API if opening the websocket failed
                //  This may happen if the shared document is not a YDocument.
                console.error(`Failed to open websocket connection for ${options.path}.\n:${error}`);
            }
        };
        this._user = user;
        this._trans = translator;
        this._providers = new Map();
        this.sharedModelFactory = new SharedModelFactory(this._onCreate);
    }
    /**
     * Dispose of the resources held by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._providers.forEach(p => p.dispose());
        this._providers.clear();
        super.dispose();
    }
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     *
     * Uses the [Jupyter Notebook API](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter/notebook/master/notebook/services/api/api.yaml#!/contents) and validates the response model.
     */
    async get(localPath, options) {
        if (options && options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                // If the document does't exist, `super.get` will reject with an
                // error and the provider will never be resolved.
                // Use `Promise.all` to reject as soon as possible. The Context will
                // show a dialog to the user.
                const [model] = await Promise.all([
                    super.get(localPath, { ...options, content: false }),
                    provider.ready
                ]);
                return model;
            }
        }
        return super.get(localPath, options);
    }
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    async save(localPath, options = {}) {
        // Check that there is a provider - it won't e.g. if the document model is not collaborative.
        if (options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._providers.get(key);
            if (provider) {
                // Save is done from the backend
                const fetchOptions = {
                    type: options.type,
                    format: options.format,
                    content: false
                };
                return this.get(localPath, fetchOptions);
            }
        }
        return super.save(localPath, options);
    }
}
/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory {
    /**
     * Shared model factory constructor
     *
     * @param _onCreate Callback on new document model creation
     */
    constructor(_onCreate) {
        this._onCreate = _onCreate;
        /**
         * Whether the IDrive supports real-time collaboration or not.
         */
        this.collaborative = !DISABLE_RTC;
        this._documentFactories = new Map();
    }
    /**
     * Register a SharedDocumentFactory.
     *
     * @param type Document type
     * @param factory Document factory
     */
    registerDocumentFactory(type, factory) {
        if (this._documentFactories.has(type)) {
            throw new Error(`The content type ${type} already exists`);
        }
        this._documentFactories.set(type, factory);
    }
    /**
     * Create a new `ISharedDocument` instance.
     *
     * It should return `undefined` if the factory is not able to create a `ISharedDocument`.
     */
    createNew(options) {
        if (typeof options.format !== 'string') {
            console.warn(`Only defined format are supported; got ${options.format}.`);
            return;
        }
        if (!this.collaborative || !options.collaborative) {
            // Bail if the document model does not support collaboration
            // the `sharedModel` will be the default one.
            return;
        }
        if (this._documentFactories.has(options.contentType)) {
            const factory = this._documentFactories.get(options.contentType);
            const sharedModel = factory(options);
            this._onCreate(options, sharedModel);
            return sharedModel;
        }
        return;
    }
}
