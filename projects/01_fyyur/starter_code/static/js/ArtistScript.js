const deleteLink = document.querySelectorAll('.delete-link');
  for (let i = 0; i < deleteLink.length; i++) {
    const lnk = deleteLink[i];
    lnk.onclick = function(e) {
      const artistId = Number(e.target.dataset['id']);
      fetch('/artists/' + artistId, {
        method: 'DELETE'
      }).then(function(){document.location.reload(true);})
    }
  }