async function recommend() {
    var anime_name = document.getElementById("anime_name").value;
    console.log(anime_name);

    const data = {
        name: anime_name
    };

    try{
        const response = await fetch('http://localhost:5011/anifinder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log(result);

        const div = document.getElementById("results");

        div.innerHTML = '';

        result.list.forEach(anime => {
            const p = document.createElement("p");

            p.textContent = anime;

            div.appendChild(p);
        });

    } catch (error) {
        console.error('Erro:', error);
    }
}