$(document).ready(function() {
    $("#chat-widget-button").on("click", function() {
        $("#chat-widget").toggleClass("d-none");
    });

    $("#chat-widget-close-button").on("click", function() {
        $("#chat-widget").addClass("d-none");
    });

    function sendMessage() {
        let userMessage = $("#chat-widget-input").val();
        $("#chat-widget-input").val("");

        // Ajouter le message de l'utilisateur à l'interface
        $("#chat-widget-messages").append("<div class='message-container user-message'><img src='static/images/user.png' alt='User'><div><strong>Vous:</strong> " + userMessage + "</div></div>");

        // Ajouter les points de suspension animés
        let typingDots = $("<div class='message-container assistant-message'><div><strong>Assistant:</strong> <span id='typing-dots' class='typing-dots'><span class='dot'></span><span class='dot'></span><span class='dot'></span></span></div><img src='static/images/robot.png' alt='Bot'></div>");
        $("#chat-widget-messages").append(typingDots);
        $("#chat-widget-messages").animate({ scrollTop: $("#chat-widget-messages")[0].scrollHeight }, 1000);

        // Envoyer le message de l'utilisateur au serveur Flask
        $.ajax({
            type: "POST",
            url: "/webhook",
            contentType: "application/json",
            data: JSON.stringify({ message: userMessage }),
            success: function(data) {
                // Supprimer les points de suspension animés une fois que la réponse est prête
                typingDots.remove();

                // Ajouter la réponse du bot à l'interface
                if (data.unknown) {
                    $("#chat-widget-messages").append("<div class='message-container assistant-message'><div><strong>Assistant:</strong> Désolé, je n'ai pas la réponse à cette question.</div><img src='static/images/robot.png' alt='Bot'></div>");
                } else {
                    data.responses.forEach(function(response) {
                        let messageHtml = "<div class='message-container assistant-message'><div><strong>Assistant:</strong> " + response.text + "</div><img src='static/images/robot.png' alt='Bot'></div>";
                        if (response.buttons) {
                            messageHtml += "<div>";
                            response.buttons.forEach(function(button) {
                                messageHtml += "<button class='chat-button' data-url='" + button.payload + "'>" + button.title + "</button>";
                            });
                            messageHtml += "</div>";
                        }
                        $("#chat-widget-messages").append(messageHtml);
                    });

                    // Ajouter un gestionnaire d'événements aux nouveaux boutons
                    $(".chat-button").off("click").on("click", function() {
                        let url = $(this).data("url");
                        window.open(url, "_blank");
                    });
                }

                // Faire défiler vers le bas pour voir la nouvelle réponse
                $("#chat-widget-messages").animate({ scrollTop: $("#chat-widget-messages")[0].scrollHeight }, 1000);
            },
            error: function() {
                // Gérer l'erreur si nécessaire
                typingDots.remove();
                $("#chat-widget-messages").append("<div class='message-container assistant-message'><div><strong>Assistant:</strong> Désolé, une erreur est survenue. Veuillez réessayer plus tard.</div><img src='static/images/robot.png' alt='Bot'></div>");
                // Faire défiler vers le bas pour voir le message d'erreur
                $("#chat-widget-messages").animate({ scrollTop: $("#chat-widget-messages")[0].scrollHeight }, 1000);
            }
        });
    }

    $("#chat-widget-send-button").on("click", function() {
        sendMessage();
    });

    $("#chat-widget-input").keypress(function(event) {
        if (event.which === 13) {
            sendMessage();
        }
    });
});
