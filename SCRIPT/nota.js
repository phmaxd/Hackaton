fetch('../python/scrypt.php')
    .then(response => response.json())
    .then(data => {
     return fetch('../PHP/salvar.php',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: data})
     });
    })
    .then(response => response.text())
    .then(result => {
        console.log('Success:', result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
