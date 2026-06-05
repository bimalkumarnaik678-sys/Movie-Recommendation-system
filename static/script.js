async function recommendMovie() {

    const movie =
        document.getElementById("movie").value;

    if(movie.trim() === "") {

        alert("Please enter a movie name");

        return;
    }

    const container =
        document.getElementById(
            "recommendations"
        );

    container.innerHTML =
        `<div class="loading">
            Finding Similar Movies...
         </div>`;

    try {

        const response =
            await fetch("/recommend", {

            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                movie:movie
            })

        });

        const data =
            await response.json();

        container.innerHTML = "";

        if(!data.success){

            container.innerHTML = `
                <h2>
                ${data.error}
                </h2>
            `;

            return;
        }

        data.movies.forEach(movie => {

            container.innerHTML += `

            <div class="movie-card">

                <div class="movie-info">

                    <h3>
                    ${movie.title}
                    </h3>

                    <p>
                    Recommended for you
                    </p>

                </div>

            </div>
            `;
        });

    }

    catch(error){

        container.innerHTML = `
        <h2>
        Server Error
        </h2>
        `;

        console.error(error);
    }
}