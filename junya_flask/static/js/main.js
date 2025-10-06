document.getElementById("registerForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const formData = new FormData(this);

  fetch("/register", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    if (data.errors) {
      const messages = Object.values(data.errors).join("\n");
      alert(messages);
    } else if (data.success) {
      location.href = "/";
    }
  })
  .catch(() => {
    alert("通信エラーが発生しました");
  });
}); 