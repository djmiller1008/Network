document.addEventListener("DOMContentLoaded", () => {
    
    const editButtons = document.querySelectorAll('.edit');
   
    editButtons.forEach(editButton => {
        const index = editButton.dataset.index;
      
        editButton.addEventListener('click', () => {
            const postContentTag = document.getElementById(index)
            const textArea = document.createElement('textarea');
           
            textArea.innerHTML = postContentTag.innerHTML
    
            postContentTag.parentNode.replaceChild(textArea, postContentTag)
            editButton.innerHTML = 'Save'
        })

    })
})