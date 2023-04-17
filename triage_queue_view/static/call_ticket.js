function processarFormulario(form) {
    // Obter os valores dos campos ocultos
    
    var nome = form.elements["name"].value;
    var documentNumber = form.elements["document_number"].value;
    
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
    
    var urlencoded = new URLSearchParams();
    urlencoded.append("name", nome);
    urlencoded.append("document_number", documentNumber);
    
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: urlencoded,
      redirect: 'follow'
    };
    fetch("http://127.0.0.1:5000/call", requestOptions)
      .then(response => response.text())
      .then(result => console.log(result))
      .catch(error => console.log('error', error));

      window.location.href('queue')
}