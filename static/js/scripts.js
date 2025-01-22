document.getElementById('fetch-employers').addEventListener('click', function () {
    fetch('/api/employers')
        .then(response => response.json())
        .then(data => {
            const employerList = document.getElementById('employer-list');
            employerList.innerHTML = data.map(e => `<p>${e.name}</p>`).join('');
        })
        .catch(error => console.error('Error fetching employers:', error));
});
