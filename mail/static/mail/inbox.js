document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  document
    .querySelector("#compose-form")
    .addEventListener("submit", post_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function load_email(email_id) {
  // Show the mailbox and hide other views
  document.querySelector("#single-email-view").style.display = "block";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  document.querySelector("#single-email-view").innerHTML = "";

  fetch(`/emails/${email_id}`)
    .then((response) => response.json())
    .then((email) => {
      const element = document.createElement("div");

      const title = document.createElement("h3");
      title.innerHTML = email.subject;
      element.append(title);

      const recipients = document.createElement("h6");
      recipients.innerHTML = `To: ${email.recipients}`;
      element.append(recipients);

      const sender = document.createElement("h6");
      sender.innerHTML = `From: ${email.sender}`;
      element.append(sender);

      const timestamp = document.createElement("p");
      timestamp.innerHTML = email.timestamp;
      element.append(timestamp);
      
      const hr = document.createElement("hr");
      hr.style.backgroundColor = "#ececec";
      element.append(hr);

      const body = document.createElement("p");
      body.innerHTML = email.body;
      element.append(body);
      
      const replyElement = document.createElement("button");
      replyElement.innerHTML = "Reply";
      replyElement.addEventListener("click", () => {
        compose_email();
        newSubject = email.subject;
        if (!newSubject.startsWith("Re: ")) {
          newSubject = `Re: ${email.subject}`;
        }
        document.querySelector("#compose-recipients").value = email.sender;
        document.querySelector(
          "#compose-subject"
        ).value = `${newSubject}`;
        document.querySelector(
          "#compose-body"
        ).value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
      });
      element.append(replyElement);

      document.querySelector("#single-email-view").append(element);
    })
    .then(
      fetch(`/emails/${email_id}`, {
        method: "PUT",
        body: JSON.stringify({
          read: true,
        }),
      }).catch((error) => {
        document.querySelector(
          "#single-email-view"
        ).innerHTML = `An error occurred: ${error}`;
      })
    )
    .catch((error) => {
      document.querySelector(
        "#single-email-view"
      ).innerHTML = `An error occurred: ${error}`;
    });
}

function post_email(event) {
  event.preventDefault(); // Prevent default form submission

  recipients = document.querySelector("#compose-recipients").value;
  subject = document.querySelector("#compose-subject").value;
  body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      messageField = document.querySelector("#post-email-message");
      if (result.error != undefined) {
        messageField.innerHTML = result.error;
        messageField.style.color = "red";
      } else {
        messageField.innerHTML = result.message;
        messageField.style.color = "green";
      }
    })
    .catch((error) => {
      messageField = document.querySelector("#post-email-message");
      messageField.innerHTML = error.error;
      messageField.style.color = "red";
    });

  return false;
}

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#single-email-view").style.display = "none";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  // Clears message field and styling
  document.querySelector("#post-email-message").innerHTML = "";
  document.querySelector("#post-email-message").style.color = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#single-email-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      console.log(emails);
      emails.forEach((email) => {
        const element = document.createElement("div");
        element.classList.add("e13_2");

        if (email.read === true) {
          color = "#ececec";
        } else {
          color = "#1c1c1c";
        }

        const title = document.createElement("span");
        title.className = "e13_3";
        title.style.color = color;
        title.innerHTML = email.subject;
        title.addEventListener("click", () => {
          load_email(email.id);
        });
        element.append(title);

        const recipients = document.createElement("span");
        recipients.className = "e13_16";
        recipients.style.color = color;
        recipients.innerHTML = `To: ${email.recipients}`;
        element.append(recipients);

        const sender = document.createElement("span");
        sender.className = "e13_4";
        sender.style.color = color;
        sender.innerHTML = `From: ${email.sender}`;
        element.append(sender);

        const body = document.createElement("span");
        body.className = "e13_15";
        body.style.color = color;
        body.innerHTML = email.body;
        element.append(body);

        const timestamp = document.createElement("span");
        timestamp.className = "e13_14";
        timestamp.style.color = color;
        timestamp.innerHTML = email.timestamp;
        element.append(timestamp);

        const readElement = document.createElement("div");
        readElement.classList = "e13_5";
        if (email.read === true) {
          readElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 20 20"><path fill="${color}" d="M10.257 3.071a.5.5 0 0 0-.514 0L2.97 7.134a1.999 1.999 0 0 0-.7.709L10 11.934l7.728-4.091a2 2 0 0 0-.699-.709l-6.772-4.063ZM18 8.831l-7.766 4.11a.5.5 0 0 1-.468 0L2 8.832V14.5A2.5 2.5 0 0 0 4.5 17h11a2.5 2.5 0 0 0 2.5-2.5V8.83Z"/></svg>`;
        } else {
          element.style.backgroundColor = "#ececec";
          readElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 20 20"><path fill="${color}" d="M18 7.373V14.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 2 14.5V7.373l7.746 4.558a.5.5 0 0 0 .508 0L18 7.373ZM15.5 4a2.5 2.5 0 0 1 2.485 2.223L10 10.92L2.015 6.223A2.5 2.5 0 0 1 4.5 4h11Z"/></svg>`;
        }

        readElement.addEventListener("click", () => {
          fetch(`/emails/${email.id}`, {
            method: "PUT",
            body: JSON.stringify({
              read: !email.read,
            }),
          });
          load_mailbox(mailbox);
        });
        element.append(readElement);

        if (mailbox === "inbox" || mailbox === "archive") {
          const archivedElement = document.createElement("div");
          archivedElement.className = "e13_9";
          archivedElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 256 256"><path fill="${color}" d="M224 48H32a16 16 0 0 0-16 16v24a16 16 0 0 0 16 16v88a16 16 0 0 0 16 16h160a16 16 0 0 0 16-16v-88a16 16 0 0 0 16-16V64a16 16 0 0 0-16-16Zm-16 144H48v-88h160Zm16-104H32V64h192v24ZM96 136a8 8 0 0 1 8-8h48a8 8 0 0 1 0 16h-48a8 8 0 0 1-8-8Z"/></svg>`;
          archivedElement.addEventListener("click", () => {
            fetch(`/emails/${email.id}`, {
              method: "PUT",
              body: JSON.stringify({
                archived: !email.archived,
              }),
            });
            load_mailbox(mailbox);
          });
          element.append(archivedElement);
        }

        document.querySelector("#emails-view").append(element);
      });
    });
}
