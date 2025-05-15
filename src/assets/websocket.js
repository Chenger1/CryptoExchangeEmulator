function WebsocketHandler(){
    this.connection = null;
    this.signalForm = document.getElementById('signalForm');

    this.connect = function(){
        this.connection = new WebSocket("ws://localhost:8000/ws");
        this.connection.onmessage = function(e){ console.log(e.data); };
        this.connection.onopen = () => this.onOpen();
    }

    this.onOpen = function(){
        this.connection.send('hello');

        const This = this;
        document.getElementById('sendSignal').addEventListener('click', function(){
            const signal = {
                'topic': 'userSignal',
                'signal': This.signalForm.signal.value
            }
            This.connection.send(JSON.stringify(signal));
        })
    }
}
