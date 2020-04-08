import dtlpy as dl
from PIL import Image, ExifTags
import logging
import io

logger = logging.getLogger(name=__name__)


class ServiceRunner(dl.BaseServiceRunner):
    """
    Package runner class

    """
    def __init__(self, **kwargs):
        """
        Init package attributes here
        
        :param kwargs: config params
        :return:
        """
        pass

    def run(self, item, progress):
        """
        Write your main service function here

        :param progress: Use this to update the progress of your package
        :return:
        """
        # check that item does not exceed maximum size
        if item.size/1000000 > 150:
            logger.warning('Cannot run service on items larger than 150MB')
            raise Exception('Cannot run service on items larger than 150MB')

        # download item and save to buffer
        try:
            buffer = item.download(local_path='/', save_locally=False)
        except dl.exceptions.NotFound:
            logger.warning('Item not found. item.filename: {}, item_id: {}'.format(item.filename, item.id))
            raise Exception('Item not found')
        except Exception:
            logger.exception('Error downloading item')
            raise Exception('Error downloading item')

        try:
            # open item buffer
            try:
                img = Image.open(buffer)
            except Exception:
                logger.error('Failed loading image')
                raise

            # run exif process
            output = dict()
            try:
                if hasattr(img, '_getexif'):
                    exif_data = img._getexif()
                    if exif_data:
                        exif = {
                            ExifTags.TAGS[k]: v
                            for k, v in exif_data.items()
                            if k in ExifTags.TAGS
                        }
                        # recursively convert all bytes to strings
                        if 'Orientation' in exif:
                            output = {'Orientation': exif['Orientation']}
            except Exception:
                logger.exception('Exception raised while fetching exif')
                raise

            try:
                # edit metadata
                if 'system' not in item.metadata:
                    item.metadata['system'] = dict()
                item.metadata['system']['exif'] = output
                item.metadata['system']['width'] = img.size[0]
                item.metadata['system']['height'] = img.size[1]
                item.update(system_metadata=True)
            except Exception:
                logger.exception('Exception raised while updating item')
                raise
        finally:
            if isinstance(buffer, io.BytesIO):
                buffer.close()
