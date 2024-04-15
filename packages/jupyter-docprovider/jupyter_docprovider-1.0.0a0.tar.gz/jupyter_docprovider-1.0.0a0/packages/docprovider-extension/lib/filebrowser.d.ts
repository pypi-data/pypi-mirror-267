import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';
import { ICollaborativeDrive } from '@jupyter/docprovider';
/**
 * The default collaborative drive provider.
 */
export declare const drive: JupyterFrontEndPlugin<ICollaborativeDrive>;
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
export declare const yfile: JupyterFrontEndPlugin<void>;
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
export declare const ynotebook: JupyterFrontEndPlugin<void>;
/**
 * The default file browser factory provider.
 */
export declare const defaultFileBrowser: JupyterFrontEndPlugin<IDefaultFileBrowser>;
/**
 * The default collaborative drive provider.
 */
export declare const logger: JupyterFrontEndPlugin<void>;
