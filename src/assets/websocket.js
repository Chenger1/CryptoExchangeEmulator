function WebsocketHandler(){
    this.connection = null;
    this.signalForm = document.getElementById('signalForm');
    this.buttons = document.getElementsByClassName('btn-check');

    this.connect = function(){
        this.connection = new WebSocket("ws://localhost:8000/ws");
        this.connection.onmessage = function(e){ console.log(e.data); };
        this.connection.onopen = () => this.onOpen();
    }

    this.onOpen = function(){
        const This = this;
        document.getElementById('sendSignal').addEventListener('click', function(){
            const exchange = Array.from(This.buttons).find(button => button.checked).id;
            const signal = {
                'topic': 'userSignal',
                'exchange': exchange,
                'signal': This.signalForm.signal.value
            }
            This.connection.send(JSON.stringify(signal));
        })
    }
}
