/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { Stream } from '@lumino/signaling';
import * as decoding from 'lib0/decoding';
import * as encoding from 'lib0/encoding';
import { WebsocketProvider } from 'y-websocket';
import { MessageType } from './utils';
/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
export class WebSocketAwarenessProvider extends WebsocketProvider {
    /**
     * Construct a new WebSocketAwarenessProvider
     *
     * @param options The instantiation options for a WebSocketAwarenessProvider
     */
    constructor(options) {
        super(options.url, options.roomID, options.awareness.doc, {
            awareness: options.awareness
        });
        this._isDisposed = false;
        this._awareness = options.awareness;
        this._user = options.user;
        this._user.ready
            .then(() => this._onUserChanged(this._user))
            .catch(e => console.error(e));
        this._user.userChanged.connect(this._onUserChanged, this);
        this._messageStream = new Stream(this);
        this.messageHandlers[MessageType.CHAT] = (encoder, decoder, provider, emitSynced, messageType) => {
            const content = decoding.readVarString(decoder);
            const data = JSON.parse(content);
            this._messageStream.emit(data);
        };
    }
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A signal to subscribe for incoming messages.
     */
    get messageStream() {
        return this._messageStream;
    }
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._user.userChanged.disconnect(this._onUserChanged, this);
        this._isDisposed = true;
        this.destroy();
    }
    /**
     * Send a message to every collaborator.
     *
     * @param msg message
     */
    sendMessage(msg) {
        const data = {
            type: 'text',
            body: msg
        };
        const encoder = encoding.createEncoder();
        encoding.writeVarUint(encoder, MessageType.CHAT);
        encoding.writeVarString(encoder, JSON.stringify(data));
        this.ws.send(encoding.toUint8Array(encoder));
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}
