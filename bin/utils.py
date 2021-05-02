'''
utilities
'''
import yaml


def parse_metadata(doc,join='\n'):
    """
    Parse the metadata from a document and parse it
    as a YAML dict and return it.
    """
    doc = doc.strip()
    if doc.startswith('---\n') and ('...' in doc or '---' in doc[4:]):
        # found starting yaml block
        yblock = doc[4:].split('...')[0].split('---')[0]
        meta = yaml.load(yblock, Loader=yaml.SafeLoader)
        for k in meta.keys():
            val = meta[k]
            if isinstance(val,list):
                meta[k] = join.join(val)
        meta['metadata_yaml_length'] = len(yblock) + 7
        if 'description' not in meta:
            body = doc[meta['metadata_yaml_length']:]
            first_para = body.strip().split('\n')[0]
            meta['description'] = first_para
        return meta
    else:
        # No yaml
        return {}

