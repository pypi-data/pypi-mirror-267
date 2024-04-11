(() => {
  function getRequest (btn) {
    const form = new FormData()
    form.append('object_id', btn.dataset.objectId)
    form.append('model_label', btn.dataset.modelLabel)
    return new Request(btn.dataset.url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: form,
      mode: 'same-origin'
    })
  }

  function getModelContainer (btn) {
    return btn.closest('.model-watchlist-container')
  }

  function removeModel (btn) {
    getModelContainer(btn).remove()
    if (!document.querySelector('.model-watchlist-container')) {
      const emptyMessage = document.getElementById('empty-watchlist')
      emptyMessage.style = 'display: block;'
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    // Add handler for the toggle button:
    document.querySelectorAll('.watchlist-toggle-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault()
        fetch(getRequest(btn))
          .then(response => {
            if (!response.ok) {
              throw new Error(`Toggle response was not ok (status code: ${response.status})`)
            }
            return response.json()
          })
          .then(data => {
            if (data.on_watchlist) {
              btn.classList.remove('text-primary')
              btn.classList.add('text-success')
              btn.classList.add('on-watchlist')
            } else {
              btn.classList.add('text-primary')
              btn.classList.remove('text-success')
              btn.classList.remove('on-watchlist')
            }
          })
          .catch((error) => console.log(`Error when toggling watchlist: ${error}`))
      })
    })

    // Add handler for the remove button:
    document.querySelectorAll('.watchlist-remove-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault()
        fetch(getRequest(btn))
          .then(response => {
            if (response.ok) {
              if (btn.closest('.watchlist-items-list').children.length === 1) {
              // This is the only watchlist item for that model - remove the
              // model container.
                removeModel(btn)
              } else {
              // Remove just this watchlist item.
                btn.closest('.watchlist-item').remove()
              }
            }
          })
          .catch((error) => console.log(`Error when removing watchlist item: ${error}`))
      })
    })

    // Add handler for the 'remove all' buttons that remove all watchlist items
    // of a particular model.
    document.querySelectorAll('.watchlist-remove-all-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault()
        fetch(getRequest(btn))
          .then(response => { if (response.ok) { removeModel(btn) } })
          .catch((error) => console.log(`Error when removing all watchlist items: ${error}`))
      })
    })
  })
})()
