const definitions = {}

definitions.permissions = {
  POST_IMAGES: 'post:images',
  DELETE_IMAGES: 'delete:images',
  POST_ALBUMS: 'post:albums',
  DELETE_ALBUMS: 'delete:albums',
  PATCH_ALBUM: 'patch:albums'
}

definitions.checkpoints = {
  ALBUMS: '/albums',
  IMAGES: '/images'
}

definitions.messages = {
  NO_IMAGES_MESSAGE: 'No images found',
  NO_ALBUMS_FOUND: 'No albums found.',
  CREATE_ALBUM_BUTTON_TEXT: 'Create Album',
  UPLOAD_IMAGE_BUTTON_TEXT: 'Upload Image',
  ALBUMS_LIST_HEADER: 'Albums available:',
  IMAGES_LIST_HEADER: ''
}

definitions.id = {
  LOGIN_BUTTON: 'login_button_id',
  LOGOUT_BUTTON: 'logout_button_id',
  NO_IMAGE_HTML_MESSAGE: 'hidden_message_id',
  IMAGE_LIST: 'image_list_id',
  ALBUMS_LIST_MAIN_DIV: 'albums_list_main_div_id',
  IMAGES_LIST_MAIN_DIV: 'albums_list_main_div_id'
}

definitions.classes = {
  DELETE_BUTTON: 'delete_button',
  RENAME_FIELD: 'rename_button'
}

definitions.attributes = {
  RENAME_ATTR: 'renameattr'
}

definitions.images = {
  MAX_SIDE: 200
}
