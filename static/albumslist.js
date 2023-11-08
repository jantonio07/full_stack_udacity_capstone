class BaseList {
  constructor (oViewModel, oParams, elParent) {
    this.sMainDivId = oParams.mainDivId
    const elMainDiv = document.createElement('div')
    elMainDiv.id = this.sMainDivId
    elParent.appendChild(elMainDiv)

    this.checkpoint = oParams.checkpoint
    this.oViewModel = oViewModel
    this.oParams = oParams

    this.createUploader(elMainDiv, oParams)
    this.createList(elMainDiv, oParams)
  }

  getListId () {
    return this.sMainDivId + '_listelement_id'
  }

  getEmptyListMessageId () {
    return this.sMainDivId + '_noelementmessage_id'
  }

  createUploader (elMainDiv, oParams) {
    const elForm = document.createElement('form')
    elForm.style.marginTop = '15px'
    elMainDiv.appendChild(elForm)

    const elInput = document.createElement('input')
    elInput.setAttribute('type', oParams.inputType)
    elInput.setAttribute('name', oParams.inputName)
    elForm.appendChild(elInput)

    const elbutton = document.createElement('button')
    elbutton.setAttribute('type', 'submit')
    elbutton.innerText = oParams.buttonText
    elForm.appendChild(elbutton)

    elForm.setAttribute('data-bind', 'visible: permissions().includes("' + oParams.postPermission + '")')
    ko.applyBindings(this.oViewModel, elForm)

    elbutton.addEventListener('click', async (evt) => {
      evt.preventDefault()
      const oFormData = this.inputHandler(elInput)
      this.fetch('POST', oParams.checkpoint, oFormData, (oResponse) => { this.addItemsToList(oResponse) })
    })
  }

  async fetch (sMethod, sCheckpoint, oFormData, fSuccessHandler) {
    const sToken = this.oViewModel.token()
    const headers = {
      Authorization: 'Bearer ' + sToken
    }
    if ((typeof oFormData) === 'string') {
      headers['Content-Type'] = 'application/json'
    }
    const oPromise = fetch(sCheckpoint, {
      method: sMethod,
      body: oFormData,
      headers
    })
    oPromise.then(oResponse => {
      const oJson = oResponse.json()
      return oJson
    })
      .then(oData => {
        console.log('Data received ' + sCheckpoint + ': ', oData)
        if (oData.success) {
          fSuccessHandler(oData)
        }
      })
      .catch(oError => {
        console.error('Error received ' + sCheckpoint + ': ', oError)
      })
    return oPromise
  }

  updateEmptyListMessage () {
    const elEmptyListMessage = document.getElementById(this.getEmptyListMessageId())
    const elList = document.getElementById(this.getListId())
    elEmptyListMessage.style.display = elList.childElementCount === 0 ? 'block' : 'none'
  }

  createList (elMainDiv, oParams) {
    const elListDiv = document.createElement('div')
    elMainDiv.appendChild(elListDiv)

    const elHeaderListMessage = document.createElement('h2')
    elHeaderListMessage.innerText = oParams.headerListMessage
    elHeaderListMessage.style.display = 'block'
    elListDiv.appendChild(elHeaderListMessage)

    const elNoImageMessage = document.createElement('h3')
    elNoImageMessage.id = this.getEmptyListMessageId()
    elNoImageMessage.innerText = oParams.emptyListMessage
    elNoImageMessage.style.display = 'block'
    elListDiv.appendChild(elNoImageMessage)

    const elList = document.createElement('ul')
    elList.id = this.getListId()
    elListDiv.appendChild(elList)

    return this.fetch('GET', oParams.checkpoint, null, (oResponse) => {
      this.addItemsToList(oResponse)
    })
  }

  removeItemFromList (oResponse, elItem) {
    elItem.remove()
    this.updateEmptyListMessage()
  }

  addDeleteButtonToListItem (elItem, databaseId) {
    const elDeleteButton = document.createElement('button')
    elDeleteButton.innerText = 'Delete'
    elDeleteButton.classList.add(definitions.classes.DELETE_BUTTON)
    elDeleteButton.style.marginLeft = '5px'
    elDeleteButton.setAttribute('data-bind', 'visible: permissions().includes("' + this.oParams.deletePermission + '")')

    elDeleteButton.style.display = 'none'
    elItem.appendChild(elDeleteButton)

    elDeleteButton.addEventListener('click', async (evt) => {
      evt.preventDefault()
      this.fetch('DELETE', this.oParams.deleteCheckpoint + '/' + databaseId, null, (oResponse) => { this.removeItemFromList(oResponse, elItem) })
    })
  }
}

class ImagesList extends BaseList {
  constructor (oViewModel, elParent) {
    const oParams = {
      mainDivId: definitions.id.IMAGES_LIST_MAIN_DIV + elParent.id,
      buttonText: definitions.messages.UPLOAD_IMAGE_BUTTON_TEXT,
      inputType: 'file',
      inputName: 'file',
      postPermission: definitions.permissions.POST_IMAGES,
      deletePermission: definitions.permissions.DELETE_IMAGES,
      checkpoint: definitions.checkpoints.ALBUMS + '/' + elParent.id + definitions.checkpoints.IMAGES,
      deleteCheckpoint: definitions.checkpoints.IMAGES,
      emptyListMessage: definitions.messages.NO_IMAGES_MESSAGE,
      headerListMessage: definitions.messages.IMAGES_LIST_HEADER
    }
    super(oViewModel, oParams, elParent)
  }

  inputHandler (elInput) {
    const oFile = elInput.files[0]
    const oFormData = new FormData()
    oFormData.append('file', oFile)
    return oFormData
  }

  addItemsToList (oData) {
    const aImages = oData.images
    const elList = document.getElementById(this.getListId())
    for (let i = 0; i < aImages.length; i++) {
      const oImage = aImages[i]
      const nMax = oImage.w > oImage.h ? oImage.w : oImage.h
      const nHeight = oImage.h * definitions.images.MAX_SIDE / nMax
      const nWidth = oImage.w * definitions.images.MAX_SIDE / nMax

      const elItem = document.createElement('li')
      elItem.setAttribute('databaseId', oImage.id)
      elItem.id = oImage.id
      elItem.style.marginBottom = '10px'
      elItem.style.display = '-webkit-box'
      elList.appendChild(elItem)

      const elImage = document.createElement('img')
      elImage.setAttribute('src', oImage.url)
      elImage.setAttribute('height', nHeight + 'px')
      elImage.setAttribute('width', nWidth + 'px')
      elItem.appendChild(elImage)

      this.addDeleteButtonToListItem(elItem, oImage.id)
      ko.applyBindings(this.oViewModel, elItem)
    }
    this.updateEmptyListMessage()
  }
}

class AlbumsList extends BaseList {
  constructor (oViewModel) {
    const oParams = {
      mainDivId: definitions.id.ALBUMS_LIST_MAIN_DIV,
      buttonText: definitions.messages.CREATE_ALBUM_BUTTON_TEXT,
      inputType: 'text',
      inputName: 'text',
      postPermission: definitions.permissions.POST_ALBUMS,
      deletePermission: definitions.permissions.DELETE_ALBUMS,
      patchPermission: definitions.permissions.PATCH_ALBUM,
      checkpoint: definitions.checkpoints.ALBUMS,
      deleteCheckpoint: definitions.checkpoints.ALBUMS,
      emptyListMessage: definitions.messages.NO_ALBUMS_FOUND,
      headerListMessage: definitions.messages.ALBUMS_LIST_HEADER
    }
    super(oViewModel, oParams, document.body)
  }

  inputHandler (elInput) {
    const sAlbumName = elInput.value
    const oJson = {
      albumName: sAlbumName
    }
    return JSON.stringify(oJson)
  }

  displayOrCloseAlbum (elItem) {
    const elLastChild = elItem.lastChild
    if (elLastChild.id.includes(definitions.id.IMAGES_LIST_MAIN_DIV)) {
      elLastChild.remove()
    } else {
      new ImagesList(this.oViewModel, elItem)
    }
  }

  addClicksLogicToListItem (elItem, databaseId) {
    const elRenameField = document.createElement('input')
    elRenameField.setAttribute('type', 'text')
    elRenameField.style.display = 'none'
    const sCondition = '(permissions().includes("' + this.oParams.patchPermission + '") ? true : false)'
    elRenameField.setAttribute('data-bind', 'attr:{ ' + definitions.attributes.RENAME_ATTR + ': ' + sCondition + ' }')

    const elItemName = elItem.firstChild
    elItem.insertBefore(elRenameField, elItem.firstChild)

    let bTriggerFirstClick = true
    elItemName.addEventListener('click', async (evt) => {
      evt.preventDefault()
      bTriggerFirstClick = true
      setTimeout(() => {
        if (bTriggerFirstClick) {
          this.displayOrCloseAlbum(elItem, databaseId)
        }
      }, 350)
    })
    elItemName.addEventListener('dblclick', async (evt) => {
      bTriggerFirstClick = false
      evt.preventDefault()

      if (elRenameField.hasAttribute(definitions.attributes.RENAME_ATTR) && elRenameField.getAttribute(definitions.attributes.RENAME_ATTR) === 'true') {
        elRenameField.style.display = ''
        elItemName.style.display = 'none'
        elRenameField.value = elItemName.innerText
        elRenameField.focus()
      }
    })
    const fRenameHandler = () => {
      const sNewName = elRenameField.value
      elRenameField.style.display = 'none'
      elItemName.style.display = ''

      const oFormData = JSON.stringify({ newName: sNewName })
      this.fetch('PATCH', this.checkpoint + '/' + databaseId, oFormData, () => {
        elItemName.innerText = sNewName
      })
    }
    elRenameField.addEventListener('blur', (evt) => {
      evt.preventDefault()
      fRenameHandler()
    })
    elRenameField.addEventListener('keyup', (evt) => {
      if (evt.key === 'Enter') {
        fRenameHandler()
      }
    })
  }

  addItemsToList (oData) {
    const aAlbums = oData.albums
    const elList = document.getElementById(this.getListId())
    for (let i = 0; i < aAlbums.length; i++) {
      const oAlbum = aAlbums[i]

      const elAlbum = document.createElement('li')
      elAlbum.setAttribute('databaseId', oAlbum.id)
      elAlbum.id = oAlbum.id
      elAlbum.style.marginBottom = '5px'

      const elText = document.createElement('span')
      elText.textContent = oAlbum.name
      elText.style.cursor = 'pointer'
      elAlbum.appendChild(elText)

      this.addClicksLogicToListItem(elAlbum, oAlbum.id)
      this.addDeleteButtonToListItem(elAlbum, oAlbum.id)
      elList.appendChild(elAlbum)
      ko.applyBindings(this.oViewModel, elAlbum)
    }
    this.updateEmptyListMessage()
  }
}
