import { User } from '@jupyterlab/services';
import { IDisposable } from '@lumino/disposable';
import { IStream } from '@lumino/signaling';
import { IAwareness } from '@jupyter/ydoc';
import { WebsocketProvider } from 'y-websocket';
import { IAwarenessProvider } from './tokens';
export interface IContent {
    type: string;
    body: string;
}
export interface IChatMessage {
    sender: string;
    timestamp: number;
    content: IContent;
}
/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
export declare class WebSocketAwarenessProvider extends WebsocketProvider implements IAwarenessProvider, IDisposable {
    /**
     * Construct a new WebSocketAwarenessProvider
     *
     * @param options The instantiation options for a WebSocketAwarenessProvider
     */
    constructor(options: WebSocketAwarenessProvider.IOptions);
    get isDisposed(): boolean;
    /**
     * A signal to subscribe for incoming messages.
     */
    get messageStream(): IStream<this, IChatMessage>;
    dispose(): void;
    /**
     * Send a message to every collaborator.
     *
     * @param msg message
     */
    sendMessage(msg: string): void;
    private _onUserChanged;
    private _isDisposed;
    private _user;
    private _awareness;
    private _messageStream;
}
/**
 * A namespace for WebSocketAwarenessProvider statics.
 */
export declare namespace WebSocketAwarenessProvider {
    /**
     * The instantiation options for a WebSocketAwarenessProvider.
     */
    interface IOptions {
        /**
         * The server URL
         */
        url: string;
        /**
         * The room ID
         */
        roomID: string;
        /**
         * The awareness object
         */
        awareness: IAwareness;
        /**
         * The user data
         */
        user: User.IManager;
    }
}
