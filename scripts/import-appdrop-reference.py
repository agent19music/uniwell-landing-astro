"""Import the inspected Framer reference into local CMS seed content.

Usage: python scripts/import-appdrop-reference.py [capture.json] [assets.json]
Assets are exported separately with the read-only Framer Agent APIs.
"""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = json.loads((Path(sys.argv[1]) if len(sys.argv)>1 else root/'reference/appdrop/framer.json').read_text())
assets = json.loads((Path(sys.argv[2]) if len(sys.argv)>2 else root/'reference/appdrop/assets.json').read_text())
nodes = {}

def walk(node):
    yield node
    for child in node.get('children', []):
        yield from walk(child)

for tree in [source['page']['children'][0], *source['components']]:
    nodes.update({node['id']: node for node in walk(tree)})

def text(node):
    if isinstance(node, str):
        node = nodes[node]
    if node['type'] == 'TextLineBreak':
        return '\n'
    return node.get('attributes', {}).get('text', '') + ''.join(text(c) for c in node.get('children', []))

def image(url, alt=''):
    filename = assets['images'].get(url, url.rsplit('/', 1)[-1].split('?')[0])
    return {'id': '', 'src': '/appdrop/' + filename, 'alt': alt}

def icon(id):
    return {'id': '', 'src': '/appdrop/' + id + '.svg', 'alt': ''}

def heading(id):
    parts = list(walk(nodes[id]))
    lead = ''.join(n.get('attributes', {}).get('text', '') for n in parts if n.get('attributes', {}).get('textColor'))
    full = text(id)
    return {'headline_lead': lead.replace('\u2028', '\n'), 'headline': full[len(lead):].replace('\u2028', '\n')}

def block(type, key, **fields):
    return {'_type': 'marketing_' + type, '_version': 1, '_key': key, 'anchor_id': key, **fields}

def card(id):
    node = nodes[id]
    texts = [n for n in walk(node) if n['type'] == 'RichTextNode']
    device = next((n for n in walk(node) if n.get('$componentDisplayName') == 'Device'), None)
    result = {'title': text(texts[0]), 'description': text(texts[1])}
    if device:
        result['image'] = image(device['attributes']['$control__image'], result['title'])
    return result

home = [
    block('hero', 'hero', headline_lead='AI that organizes', headline='your day for you.',
          subheadline=text('KTeSPPxFV'), centered=True, rating='4.8', rating_label='500K+ Downloads',
          avatars=[{'image': image(nodes[id]['attributes']['fill'])} for id in ['vNNEsizFR','YOzsdYuBG','q7QnZgzSt','jdmquqorq','uzQZnl7LX']],
          image=image(nodes['LvtXZVmXT']['attributes']['$control__image'], 'AppDrop dark task overview'),
          secondary_image=image(nodes['Ge1clQ8RG']['attributes']['$control__image'], 'AppDrop daily analysis'),
          primary_cta_label='App Store', primary_cta_url='https://framer.link/poOzPgO',
          secondary_cta_label='Google Play', secondary_cta_url='https://framer.link/poOzPgO'),
    block('statement', 'challenge', eyebrow='The Challenge', **heading('OWaUzVzcI')),
    block('benefits', 'benefits', eyebrow='Key Benefits', **heading('fB1AudSCo'),
          cards=[card(id) for id in ['eTFvI267p','vAfG8g5nL','mDBQ0aTUx']]),
]

features = nodes['hRd8cbObj']
feature_cards = []
for wrapper in [features['children'][0], features['children'][2]]:
    for item in wrapper['children']:
        result = card(item['id'])
        result['icon_image'] = icon(item['children'][0]['id'])
        result['icon'] = 'star'
        feature_cards.append(result)
home.append(block('features', 'features', eyebrow='Features', **heading('BGRdR3ydM'), features=feature_cards,
                  image=image(nodes['UGX0qePi9']['attributes']['$control__image'], 'AppDrop smart capture screen')))

intelligence = []
for id in ['AX8HGABJP','EzzO0tnnu','wwAETsCd9']:
    item = card(id)
    item['image'] = image(nodes[id]['children'][0]['attributes']['fill'], item['title'])
    intelligence.append(item)
home.append(block('intelligence','intelligence',eyebrow='Intelligence Powered',**heading('iFlJpNLVz'),cards=intelligence))

integration_controls=nodes['w5Mn7YZ5_']['attributes']
integration_names=['Notion','OpenAI','Apple Notes','Grammarly','Google Calendar','Instagram']
home.append(block('integrations','connect',eyebrow='Connect',**heading('S9oAWfVBK'),subheadline=text('ARtW2onec'),
                  integrations=[{'name': name, 'logo': image(integration_controls['$control__icon'+str(i+1)]['src'],name)} for i,name in enumerate(integration_names)]))

reviews=[]
for variant in nodes['inZCqZKR0']['children']:
    review=variant['children'][0]['attributes']
    reviews.append({'quote':review['$control__content'],'author':review['$control__name'],'role':review['$control__role'],
                    'avatar':image(review['$control__photo']['src'],review['$control__name'])})
home.append(block('testimonials','reviews',eyebrow='Hear from the people',**heading('K9SSQPKqq'),testimonials=reviews))

plans=[]
for index,card_node in enumerate(nodes['tRidPl3S6']['children'][:2]):
    details = next(n for n in card_node['children'] if n.get('name')=='Plan Details')
    wrapper = details['children'][0]
    features_node = next(n for n in details['children'] if n.get('name')=='Features')
    cta = next(n for n in details['children'] if n.get('$componentDisplayName')=='Primary Button')['attributes']
    plans.append({'name':text(wrapper['children'][0]),'price':'$0' if index==0 else '$20','yearly_price':'$0' if index==0 else '$16',
                  'period':'/month','features':'\n'.join(text(n) for n in features_node['children']),
                  'cta_label':cta['$control__label'],'cta_url':cta['$control__link'],'highlighted':index==1})
home.append(block('pricing','pricing',plans=plans, image=image('https://framerusercontent.com/images/tqqaymrX5zjGQ6nIyrWDOKkclDM.png','AppDrop task list'), yearly_label='Save 20% on yearly plan'))

faqs=[]
for n in walk(nodes['Aa7qm95P3']):
    if n.get('$componentDisplayName')=='FAQ Row':
        a=n['attributes'];faqs.append({'question':a['$control__question'],'answer':a['$control__answer']})
home.append(block('faq','faqs',eyebrow='FAQs',**heading('SLbmrxGCA'),items=faqs,
                  support_text="If you can't find the answer or need help, email us at",support_email='help@apprdrop.com'))
steps=[]
for n in nodes['nYjTxOpsD']['children']:
    item=card(n['id']);item['icon_image']=icon(n['children'][0]['id']);steps.append(item)
home.append(block('download','download',eyebrow='4 Easy steps to get started',**heading('A0RQuoDEB'),steps=steps,
                  primary_cta_label='App Store',primary_cta_url='https://framer.link/poOzPgO',
                  secondary_cta_label='Google Play',secondary_cta_url='https://framer.link/poOzPgO'))

(root/'src/data').mkdir(exist_ok=True)
(root/'src/data/appdrop.json').write_text(json.dumps({'home':home},indent='\t',ensure_ascii=False)+'\n')

seed_path=root/'seed/seed.json'
seed=json.loads(seed_path.read_text())
seed['meta'].update(name='AppDrop',description='AppDrop Framer reference port')
seed['settings']={'title':'AppDrop','tagline':text('KTeSPPxFV')}
for page in seed['content']['pages']:
    if page['slug']=='home':
        page['data']['content']=home
    elif page['slug']=='pricing':
        page['data']['content']=[block('hero','pricing-intro',headline_lead='Simple pricing.',headline='Start for free.',centered=True),home[7],home[8]]
    elif page['slug']=='contact':
        page['data']['content']=[block('hero','contact',headline_lead='Contact',headline='AppDrop',subheadline='Questions or support? Email help@appdrop.com.',centered=True,primary_cta_label='Email support',primary_cta_url='mailto:help@appdrop.com')]
seed['menus'][1]['items']=[{'type':'custom','label':label,'url':url} for label,url in [('Benefits','/#benefits'),('Features','/#features'),('Pricing','/#pricing'),('Download','/#download')]]
seed['menus'][2]['label']='Footer: More'
seed['menus'][2]['items']=[{'type':'custom','label':label,'url':url} for label,url in [('Integration','/#connect'),('Questions','/#faqs'),('Reviews','/#reviews'),('Support','mailto:help@appdrop.com')]]
seed['menus'][3]['items']=[]

def field(slug,label,type='string',**extra):return {'slug':slug,'label':label,'type':type,**extra}
def repeater(slug,label,subfields,max_items=12):return field(slug,label,'repeater',validation={'maxItems':max_items,'subFields':subfields})
common=[field('anchor_id','Anchor ID'),field('eyebrow','Section label'),field('headline_lead','Muted headline text','text'),field('headline','Headline','text')]
for b in seed['blockTypes']:
    fields=b['versions'][0]['fields']
    for f in common:
        if not any(existing['slug']==f['slug'] for existing in fields):fields.insert(0,f)
    if b['slug']=='marketing_hero':
        fields.extend([field('secondary_image','Second device screen','image'),field('rating','Rating'),field('rating_label','Rating label'),repeater('avatars','Rating portraits',[field('image','Portrait','image')],5)])
    if b['slug']=='marketing_features':
        fields.append(field('image','Device screen','image'))
        fs=next(f for f in fields if f['slug']=='features')['validation']['subFields']
        fs.append(field('icon_image','Icon artwork','image'))
    if b['slug']=='marketing_pricing':
        fields.extend([field('image','Device screen','image'),field('yearly_label','Yearly saving label')])
        next(f for f in fields if f['slug']=='plans')['validation']['subFields'].append(field('yearly_price','Yearly price'))
    if b['slug']=='marketing_faq':fields.extend([field('support_text','Support text','text'),field('support_email','Support email')])
    if b['slug']=='marketing_download':next(f for f in fields if f['slug']=='steps')['validation']['subFields'].append(field('icon_image','Icon artwork','image'))
for slug,label in [('benefits','Benefits'),('intelligence','Intelligence')]:
    seed['blockTypes'].append({'slug':'marketing_'+slug,'label':label,'category':'Marketing','currentVersion':1,'versions':[{'version':1,'fields':[*common,repeater('cards','Cards',[field('title','Title',required=True),field('description','Description','text'),field('image','Artwork','image')],3)]}]})
allowed=next(f for f in seed['collections'][0]['fields'] if f['slug']=='content')['validation']['allowedTypes']
allowed.extend(['marketing_benefits','marketing_intelligence'])
# Repeated scans update the same schema instead of duplicating fields/types.
def unique(items, key):
    return list({item[key]:item for item in reversed(items)}.values())[::-1]
seed['blockTypes']=unique(seed['blockTypes'],'slug')
for block_type in seed['blockTypes']:
    for version in block_type['versions']:
        version['fields']=unique(version['fields'],'slug')
        for f in version['fields']:
            if f.get('validation',{}).get('subFields'):
                f['validation']['subFields']=unique(f['validation']['subFields'],'slug')
allowed[:]=dict.fromkeys(allowed)
seed_path.write_text(json.dumps(seed,indent='\t',ensure_ascii=False)+'\n')
print('Imported',len(home),'original page sections.')
