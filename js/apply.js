window.addEventListener( "load", function () {
    function sendData(data) {
      const XHR = new XMLHttpRequest();

      // TODO: handle modal close when response code = 200

      // Define what happens on successful data submission
      XHR.addEventListener( "load", function(event) {
        var reliefApplicationModal = document.getElementById( "relief-application-modal" );
        var reliefApplicationModalInstance = M.Modal.getInstance(reliefApplicationModal);
        var giftCardApplicationModal = document.getElementById( "gift-card-application-modal" );
        var giftCardApplicationModalInstance = M.Modal.getInstance(giftCardApplicationModal);
        if (reliefApplicationModalInstance.isOpen) {
          reliefApplicationModalInstance.close();
        } else if (giftCardApplicationModalInstance.isOpen) {
          giftCardApplicationModalInstance.close()
        }
        alert( event.target.responseText );
      } );

      // Define what happens in case of error
      XHR.addEventListener( "error", function( event ) {
        alert( 'Oops! Something went wrong. Please try again later.' );
      } );

      // Set up our request
      // XHR.open( "POST", "https://xjgwkkfzr7.execute-api.us-east-1.amazonaws.com/pre-dev/donate" );
      XHR.open( "POST", "https://xjgwkkfzr7.execute-api.us-east-1.amazonaws.com/prod/apply" );
      XHR.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      // The data sent is what the user provided in the form
      XHR.send( JSON.stringify( data ) );
    }
  
    // Access the form element...
    let reliefApplicationForm = document.getElementById( "relief-application-form" );
    let giftCardApplicationForm = document.getElementById( "gift-card-application-form" );

    // ...and take over its submit event.
    reliefApplicationForm.addEventListener( "submit", function ( event ) {
      event.preventDefault();
      // TODO: Data validation (e.g. ensure phone numbers are phone numbers, emails are emails, data is present, etc.)
      const data = {
        "name": event.target.elements[0].value,
        "email": event.target.elements[1].value,
        "phone": event.target.elements[2].value,
        "business_url": event.target.elements[3].value,
        "gift_card_url": event.target.elements[4].value,
        "goal": event.target.elements[5].value,
        "number_of_employees": event.target.elements[6].value,
        "story": event.target.elements[7].value
      };
      console.log(data);
      sendData( data );
    } );

    giftCardApplicationForm.addEventListener( "submit", function ( event ) {
      event.preventDefault();
      // TODO: Data validation (e.g. ensure phone numbers are phone numbers, emails are emails, data is present, etc.)
      const data = {
        "name": event.target.elements[0].value,
        "email": event.target.elements[1].value,
        "phone": event.target.elements[2].value,
        "business_url": event.target.elements[3].value,
        "gift_card_url": event.target.elements[4].value,
      };
      console.log(data);
      sendData( data );
    } );
  } );