function WebsocketHandler(){
    this.connection = null;
    this.signalForm = document.getElementById('signal-form');
    this.buttons = document.getElementsByClassName('btn-check');
    this.connectionStatus = document.getElementById('connection-status')

    this.connect = function(){
        this.connection = new WebSocket("ws://localhost:8000/ws");
        this.connection.onmessage = function(e){ console.log(e.data); };
        this.connection.onopen = () => this.onOpen();
    }

    this.onOpen = function(){
        const This = this;
        This.connectionStatus.innerHTML = 'Connected';
        This.connectionStatus.classList.add('text-success');
        This.connectionStatus.classList.remove('text-warning');

        document.getElementById('send-signal').addEventListener('click', function(){
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
