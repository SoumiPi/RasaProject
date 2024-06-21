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

            // Ajouter le message de l'utilisateur à l'interface
            $("#chat-widget-messages").append("<div class='message-container user-message'><img src='static/images/user.png' alt='User'><div><strong>Vous:</strong> " + userMessage + "</div></div>");

            // Envoyer le message de l'utilisateur au serveur Flask
            $.ajax({
                type: "POST",
                url: "/webhook",
                contentType: "application/json",
                data: JSON.stringify({ message: userMessage }),
                success: function(data) {
                    // Ajouter la réponse du bot à l'interface
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

                    // Faire défiler vers le bas pour voir la nouvelle réponse
                    $("#chat-widget-messages").animate({ scrollTop: $("#chat-widget-messages")[0].scrollHeight }, 1000);
                },
                error: function() {
                    // Gérer l'erreur si nécessaire
                    $("#chat-widget-messages").append("<div class='message-container assistant-message'><img src='static/images/robot.png' alt='Bot'><div><strong>Assistant:</strong> Désolé, une erreur est survenue. Veuillez réessayer plus tard.</div></div>");
                    // Faire défiler vers le bas pour voir le message d'erreur
                    $("#chat-widget-messages").animate({ scrollTop: $("#chat-widget-messages")[0].scrollHeight }, 1000);
                }
            });
        }
    });
});
