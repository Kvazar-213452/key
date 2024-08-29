function deleteData_1(key) {
    fetch('/delete_data', {
        method: 'POST',
        body: JSON.stringify({key: key}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        location.reload(); 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function deleteData(key) {
    let modalHtml = `
        <div class="modal">
            <div class="modal-content">
            <span class="close" onclick="app_closeModal()">&times;</span>
                <p class="maint_p">Confirm the deletion</p>
                <br><br>
                <button onclick="deleteData_1('${key}')" class="vffwe">Remove</button>
                <button onclick="app_closeModal()" class="ccww">I accidentally</button>
            </div>
        </div>
    `;

    $('body').append(modalHtml);

    let modalStyle = `
        .modal {
            display: block;
            position: fixed;
            z-index: 10000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.4);
        }

        .modal-content {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 200px;
            overflow-y: hidden; 
            overflow-x: hidden;
            padding: 20px;
            background-color: #14171f;
        }

        .close {
            color: #aaa;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.5s;
            position: fixed;
            top: 0;
            right: 5px;
            z-index: 100000000000;
        }

        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }
    `;

    $('<style>').html(modalStyle).appendTo('head');
}

function app_closeModal() {
    $('.modal').remove();
}

function addData() {
    var key = document.getElementById("key").value;
    var value = document.getElementById("value").value;

    var formData = new FormData();
    formData.append('key', key);
    formData.append('value', value);

    fetch('/add_data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        location.reload(); 
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function start() {
    fetch('/start', {
        method: 'POST',
        body: 1
    })
    .then(response => response.json())
    .then(data => {
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function stop() {
    fetch('/stop', {
        method: 'POST',
        body: 1
    })
    .then(response => response.json())
    .then(data => {
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

fetch('/get_data')
.then(response => response.json())
.then(data => {
    var list = document.getElementById('list');
    for (const [key, value] of Object.entries(data)) {
        var listItem = document.createElement('div');
        listItem.textContent = `${key}: ${value}`;
        var deleteButton = document.createElement('button');
        deleteButton.className = 'aaa';
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function() {
            deleteData(key);
        };
        listItem.appendChild(deleteButton);
        list.appendChild(listItem);
    }
})
.catch(error => {
    console.error('Error:', error);
});