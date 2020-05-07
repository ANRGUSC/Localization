module.exports = function(client, io) {
    // record a list of clients subscribe to each channel
    let subscription = [];
    // map from socketId to sessionId
    let socketToChannel = [];

    const prefix = 'localization/result/';
    // socket.io function: keep track of lczn-client's activity using web socket
    io.on('connection', (socket) => {
        // record the channel number in handshake
        let channel = socket.handshake.query['subscribe'];
        channel = prefix+channel;
        console.log('handshake channel '+channel+' '+'socket id '+ socket.id);
        socketToChannel[socket.id] = channel;
        if(channel in subscription) {
            subscription[channel].push(socket.id);
        } else {
            let clients = [];
            clients.push(socket.id);
            subscription[channel] = clients
        }
        // keep track of recent activity of each client. remove them from subscription when they leave
        socket.on('disconnect', function() {
            let channel = socketToChannel[socket.id];
            console.log('socket ' + socket.id + ' disconnected.');
            if (channel in subscription) {
                let participants = subscription[channel];
                let index = participants.indexOf(socket.id);
                if (index >= 0) {
                    participants.splice(index, 1);
                    if (participants.length == 0) {
                        console.log("last listener left.");
                        delete subscription[channel];

                    }
                }
            }
        });
    });
    // mqtt function: once connected, subscribe to all topic under "localization/result"
    client.on('connect', function () {
        console.log("connect to mqtt server");
        client.subscribe('localization/result/#');
    });
    // once receive a new message, forward them to a list of client under this channel
    client.on('message', function (channel, message) {
        if(channel in subscription) {
            forwardEvents(channel, message);
        }
    });

    function forwardEvents(channel, message) {
        let participants = subscription[channel];
        for (let i = 0; i < participants.length; i++) {
            console.log('forward message to participant '+participants[i]);
            console.log(message.toString());
            io.to(participants[i]).emit('message', message.toString());
        }
    }
};
