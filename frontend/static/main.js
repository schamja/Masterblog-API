// 1. Die Funktion muss zuerst definiert sein
function loadPosts() {
    console.log("loadPosts wurde aufgerufen");
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl)
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById('post-container');
            postContainer.innerHTML = '';
            data.forEach(post => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <button onclick="deletePost(${post.id})">Delete</button>
                `;
                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error('Fehler beim Laden:', error));
}

// 2. Dann kommt addPost
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;

    fetch(baseUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post hinzugefügt:', post);
        loadPosts(); // Hier wird sie jetzt gefunden!
    })
    .catch(error => console.error('Error:', error));
}

// 3. Delete Funktion
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;
    fetch(baseUrl + '/' + postId, { method: 'DELETE' })
        .then(() => loadPosts())
        .catch(error => console.error('Error:', error));
}