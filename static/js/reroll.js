document.getElementById('rerollButton').addEventListener('click', function(e) {
    console.log("Reroll button clicked.");
    e.preventDefault();
    fetch('/reroll')
    .then(response => response.json())
    .then(data => {
        console.log("Reroll data:", data);
        document.getElementById('score').textContent = data.score;
        document.getElementById('letters').textContent = data.letters.join(' ');
    }).catch(error => {
        console.error('Error during reroll:', error);
    });
});
