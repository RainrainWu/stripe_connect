fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  const stripe = Stripe(publicKey=data.publishable_key);
  document.querySelector("#submitBtn").addEventListener("click", () => {
    fetch("/session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});