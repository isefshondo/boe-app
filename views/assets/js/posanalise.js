const btnSignupCow = document.querySelector("#button-cadastrar")

// Get Results Route

function displayResults(nPercentage, txtSymptons, txtPhase) {
  const showPercentage = document.querySelector('#button-porcentagem');
  const complicacoesTexto = document.querySelectorAll('#titulo-text-posanalise + p')[0];
  const faseContaminacao = document.querySelectorAll('#titulo-text-posanalise + p')[1];

  showPercentage.textContent = nPercentage + "%";
  complicacoesTexto.textContent = txtSymptons;
  faseContaminacao.textContent = txtPhase;
}

fetch('http://127.0.0.1:5000/getResults/646f712bfab3e118e0f1d8a4', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(responseData => {
  const nPercentage = responseData.results.percentage;
  const futureSymptons = responseData.results.nextSymptons;
  const currentPhase = responseData.results.phase;

  displayResults(nPercentage, futureSymptons, currentPhase)
})
.catch(error => {
  console.log(error)
})

btnSignupCow.addEventListener('click', () => {
  window.location.href = '/views/signupCow.html'
})