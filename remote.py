import shutil

class Remote:
    def upload(self, image_path, image_title, image_description=None,
               category_name=None):
        raise NotImplementedError()

class Flickr(Remote):
    api_key = ''
    api_secret = ''

    def __init__(self):
        import flickrapi

        self.flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret)
        (token, frob) = self.flickr.get_token_part_one(perms='write')
        if not token:
            raw_input("Press ENTER after you authorized this program")
        self.flickr.get_token_part_two((token, frob))

    def upload(self, image_path, image_title, image_description=None,
               category_name=None):
        photo = self.flickr.upload(filename=image_path,
                title=image_title,
                description=image_description,
                is_public=0,
        )

        s, is_new = self._create_set(category_name, photo.find('photoid').text)

        if not is_new:
            self.flickr.photosets_addPhoto(photo_id=photo.find('photoid').text,
                    photoset_id=s)

    def _add_set(self, title, photo_id):
        self.flickr.photosets_create(title=title, primary_photo_id=photo_id)

    def _get_sets(self):
        return self.flickr.photosets_getList()

    def _get_set_id(self, name):
        sets = self._get_sets()

        for s in sets.findall('photosets//photoset'):
            if s.find('title').text == name:
                return s.attrib['id']

        return None

    def _create_set(self, set_name, main_photo_id):
        git_set = self._get_set_id(set_name)
        is_new = False

        if git_set is None:
            git_set = self._add_set(set_name, main_photo_id)
            is_new = True

        return (git_set, is_new)

class DummyRemote(Remote):
    def upload(self, image_path, image_title, image_description=None,
               category_name=None):
        pass

class Local(Remote):
    def upload(self, image_path, image_title, image_description=None,
               category_name=None):
        shutil.copyfile(image_path, '/tmp/test.jpg')

    def local_upload(self, image_path, destination_path='~/.roflcommits'):
        shutil.copyfile(image_path, os.path.join(destination_path, 'test.jpg'))
