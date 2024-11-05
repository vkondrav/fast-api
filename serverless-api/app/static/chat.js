function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function fetchMessages() {
    try {
        const response = await fetch('/chat/messages');
        const messages = await response.json();
        const messagesDiv = document.getElementById('messages');
        const userId = getCookie('user_id');

        messagesDiv.innerHTML = '';
        messages.forEach(message => {

            let template;

            if (message.user === userId) {
                template = document.getElementById('message-template-out').content.cloneNode(true);
            } else {
                template = document.getElementById('message-template-in').content.cloneNode(true);
            }

            const userNameElement = template.querySelector('h5');
            userNameElement.textContent = message.user;

            const messageTextElement = template.querySelector('p');
            messageTextElement.textContent = message.text;

            const messagesDiv = document.getElementById('messages');

            const chatImgElement = template.querySelector('.chat-img img');
            chatImgElement.src = `https://robohash.org/${encodeURIComponent(message.user)}.svg?size=60x60`;

            messagesDiv.appendChild(template);
        });

        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const text = messageInput.value;
    if (!text) return;

    try {
        const response = await fetch(`/chat/messages?text=${encodeURIComponent(text)}`, {
            method: 'POST'
        });

        if (response.ok) {
            messageInput.value = '';
        } else {
            console.error('Error sending message:', response.statusText);
        }

    } catch (error) {
        console.error('Error sending message:', error);
    }
}

async function subscribe() {

    const ablySubscriptionApiKey = "6NlX7w.Tz0Ysw:uX3jPm2Pxk6WrQeSxt5QcXqEKSmOB8OCDTlCstw3usg"

    const ably = new Ably.Realtime(ablySubscriptionApiKey)
    ably.connection.once("connected", () => {
        console.log("Connected to Ably!")
    })

    const channel = ably.channels.get("messages")
    await channel.subscribe("id", (message) => {
        console.log("Message received: " + message.data)
        fetchMessages()
    });
}