///CHAT SCREEN CODE


import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _messages = <String>[];
  final _textController = TextEditingController();

  //final String _baseUrl = "http://your_server_address:port/chat";

  void _sendMessage(String text) async {
    if (text.isNotEmpty) {
      setState(() {
        _messages.add(text); // Add user message locally
      });
      // Send POST request with user message
      final url = Uri.parse("https://46e2-41-237-156-184.ngrok-free.app/chat");
      final body = jsonEncode({'usermessage': text,});
      final response = await http.post(url, headers: {'Content-Type': 'application/json'}, body: body,);

      //final response = await http.post(Uri.parse(_baseUrl), body: b;

      if (response.statusCode == 200) { // Check for successful response
        final serverResponse = response.body;
        setState(() {
          _messages.add(serverResponse); // Add server response locally
        });
      } else {
        print(
            "Error sending message: ${response.statusCode} - ${response.body}");
        // Handle error gracefully, e.g., display an error message to the user
      }
      _textController.text = "";
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chat Screen'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              reverse: false, // Show newest messages at the top
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                return _buildMessageBubble(message, index % 2 == 0);
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: InputDecoration(
                      hintText: 'Type your message...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8.0),
                      ),
                    ),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: () => _sendMessage(_textController.text),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(String message, bool isUser) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(8.0),
            color: isUser ? Colors.blue[100] : Colors.grey[200],
          ),
          padding: const EdgeInsets.all(8.0),
          child: Text(message),
        ),
      ),
    );
  }
}