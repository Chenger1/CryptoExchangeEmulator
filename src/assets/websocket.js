function WebsocketHandler(){
    this.connection = null;

    this.connect = function(){
        this.connection = new WebSocket("ws://localhost:8000/ws");
        this.connection.onmessage = function(e){ console.log(e.data); };
        this.connection.onopen = () => this.connection.send('hello');
    }
}
