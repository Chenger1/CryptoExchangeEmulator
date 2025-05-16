function WebsocketHandler(){
    this.connection = null;
    this.signalForm = document.getElementById('signal-form');
    this.buttons = document.getElementsByClassName('btn-check');
    this.connectionStatus = document.getElementById('connection-status')
    this.externalSignalContainer = document.getElementById('external-signal-container');

    this.connect = function(){
        this.connection = new WebSocket("ws://localhost:8000/ws");
        this.connection.onmessage = function(e){ console.log(e.data); };
        this.connection.onopen = () => this.onOpen();
        this.connection.onmessage = (e) => this.onMessage(e);
    }

    this.onOpen = function(){
        const This = this;

        This.connectionStatus.innerHTML = 'Connected';
        This.connectionStatus.classList.add('text-success');
        This.connectionStatus.classList.remove('text-warning');

        const exchange = Array.from(This.buttons).find(button => button.checked).id;
        This.connection.send(JSON.stringify({'topic': 'userSignal', 'exchange': exchange, 'signal': 'success'}))

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

    this.onMessage = function(event){
        this.addNewExternalSignal(event);
    }

    this.addNewExternalSignal = function(signal){
        const newCard = document.createElement('div');
        newCard.classList.add('card', 'mb-1', 'external-signal-card');
        const cardBody = document.createElement('div');
        cardBody.classList.add('body');
        const content = document.createTextNode(signal.data);
        cardBody.append(content);
        newCard.append(cardBody);
        this.externalSignalContainer.prepend(newCard)
    }
}
