//PeerManager.js
class PeerManager {
    constructor() {
        this.peers = [];
    }

    addPeer(peer) {
        this.peers.push(peer);
    }

    getPeers() {
        return this.peers;
    }

}

module.exports = PeerManager;
