document.addEventListener("DOMContentLoaded", () => {
    
    const editButtons = document.querySelectorAll('.edit');
   
    editButtons.forEach(editButton => {
        const index = editButton.dataset.index;
      
        editButton.addEventListener('click', () => {
            if (editButton.innerHTML === 'Edit') {

            
                const postContentTag = document.getElementById(`${index} post-content`);
                const textArea = document.createElement('textarea');
            
                textArea.innerHTML = postContentTag.innerHTML;
                textArea.id = `${index} textarea`;
                textArea.name = 'post-content';
                textArea.className = 'post-content-textarea';
                postContentTag.style.display = 'none';

                const form = document.getElementById(`${index} form`)
                form.appendChild(textArea);

                const submit = document.createElement('input');
                submit.type = 'submit';
                submit.value = 'Enter';
                submit.className = 'btn btn-primary submit-button';
                submit.id = `${index} submit-button`;
                form.appendChild(submit);

                editButton.innerHTML = 'Cancel';
            } else {
                const textArea = document.getElementById(`${index} textarea`);
                textArea.innerHTML = '';
                textArea.remove();

                const postContentTag = document.getElementById(`${index} post-content`);
                postContentTag.style.display = 'block';
                
                const submitButton = document.getElementById(`${index} submit-button`);
                submitButton.remove()
                editButton.innerHTML = 'Edit';
            }

        })

    })
})