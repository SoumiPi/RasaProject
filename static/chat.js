$(document).ready(function() {
    $("#chat-widget-button").on("click", function() {
        $("#chat-widget").toggleClass("d-none");
    });

    $("#chat-widget-close-button").on("click", function() {
        $("#chat-widget").addClass("d-none");
    });

    $("#chat-widget-input").keypress(function(event) {
        if (event.which === 13) {
            let userMessage = $("#chat-widget-input").val();
            $("#chat-widget-input").val("");

            // Ajouter le message de l'utilisateur à la boîte de chat
            $("#chat-widget-messages").append("<div class='user-message'><strong>Vous:</strong> " + userMessage + "</div>");

            // Envoyer le message de l'utilisateur au serveur Rasa
            $.ajax({
                type: "POST",
                url: "/webhook",
                contentType: "application/json",
                data: JSON.stringify({ message: userMessage }),
                success: function(data) {
                    data.responses.forEach(function(response) {
                        // Ajouter la réponse du chat à la boîte de chat
                        let messageHtml = "<div class='assistant-message'><strong>Assistant:</strong> " + response.text + "</div>";
                        $("#chat-widget-messages").append(messageHtml);

                        // Si des boutons sont présents, les ajouter à la réponse du chat
                        if (response.buttons) {
                            let buttonsHtml = "<div class='assistant-buttons'>";
                            response.buttons.forEach(function(button) {
                                buttonsHtml += "<button class='chat-button' onclick='window.open(\"" + button.url + "\", \"_blank\")'>" + button.title + "</button>";
                            });
                            buttonsHtml += "</div>";
                            $("#chat-widget-messages").append(buttonsHtml);
                        }
                    });
                },
                error: function() {
                    // Gérer l'erreur si nécessaire
                }
            });
        }
    });
});
