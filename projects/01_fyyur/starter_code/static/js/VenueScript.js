const deleteLink = document.querySelectorAll('.delete-link');
  for (let i = 0; i < deleteLink.length; i++) {
    const lnk = deleteLink[i];
    lnk.onclick = function(e) {
      const venueId = Number(e.target.dataset['id']);
      fetch('/venues/' + venueId, {
        method: 'DELETE'
      }).then(function(){document.location.reload(true);})
    }
  }