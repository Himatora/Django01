from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from smehs.models import Actor, Age, Gender, Smeh, Type
# Create your tests here.
class SmehsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        gnd=baker.make("smehs.Gender")
        tpe=baker.make("smehs.Type")
        ag=baker.make("smehs.Age")
        actr=baker.make("smehs.Actor")
        smeh=Smeh.objects.create(
            name="Нюша",
            gender=gnd,
            type=tpe,
            age=ag,
            actor=actr,
        )
        r=self.client.get('/api/smehs/')
        data=r.json()
        print(data)
        assert smeh.name==data[0]['name']
        assert smeh.id==data[0]['id']
        assert smeh.gender.id==data[0]['gender']
        assert smeh.type.id==data[0]['type']
        assert smeh.actor.id==data[0]['actor']
        assert smeh.age.id==data[0]['age']
        assert len(data)==1
    
    def test_create_smeh(self):
        gnd=baker.make("smehs.Gender")
        tpe=baker.make("smehs.Type")
        ag=baker.make("smehs.Age")
        actr=baker.make("smehs.Actor")
        r= self.client.post("/api/smehs/",{
            "name": "Нюша",
            "gender": gnd.id,
            "type":tpe.id,
            "age":ag.id,
            "actor":actr.id
        })

        new_smeh_id=r.json()['id']

        smehs=Smeh.objects.all()
        assert len(smehs) == 1
        new_smeh=Smeh.objects.filter(id=new_smeh_id).first()
        assert new_smeh.name == 'Нюша'
        assert new_smeh.gender==gnd
        assert new_smeh.type==tpe
        assert new_smeh.age==ag
        assert new_smeh.actor==actr
    def test_delete_smeh(self):
        smehs=baker.make("Smeh",10)
        r=self.client.get('/api/smehs/')
        data=r.json()
        assert len(data)==10

        smeh_id_to_delete=smehs[3].id
        self.client.delete(f'/api/smehs/{smeh_id_to_delete}/')

        r=self.client.get('/api/smehs/')
        data=r.json()
        assert len(data)==9

        assert smeh_id_to_delete not in [i['id'] for i in data]
    def test_update_smeh(self):
        smehs=baker.make("Smeh",10)
        smeh: Smeh=smehs[2]

        r=self.client.get(f'/api/smehs/{smeh.id}/')
        data=r.json()
        assert data['name'] == smeh.name

        r=self.client.put(f'/api/smehs/{smeh.id}/',{
            "name": "Совунья"
        })
        assert r.status_code==200

        r=self.client.get(f'/api/smehs/{smeh.id}/')
        data=r.json()
        assert data['name'] == "Совунья"

        smeh.refresh_from_db()
        assert data['name']==smeh.name
class GendersViewsetTestCase(TestCase):
    def test_get_list_gender(self):
        gender=baker.make("Gender")

        r=self.client.get('/api/genders/')
        data=r.json()
        print(data)
        assert gender.name==data[0]['name']
        assert gender.id==data[0]['id']
        assert len(data)==1
    def test_create_gender(self):
        r= self.client.post("/api/genders/",{
            "name": "gender"
        })

        new_gender_id=r.json()['id']

        genders=Gender.objects.all()
        assert len(genders) == 1
        new_gender=Gender.objects.filter(id=new_gender_id).first()
        assert new_gender.name == "gender"
    def test_delete_gender(self):
        genders=baker.make("Gender",10)
        r=self.client.get('/api/genders/')
        data=r.json()
        assert len(data)==10

        gender_id_to_delete=genders[3].id
        self.client.delete(f'/api/genders/{gender_id_to_delete}/')

        r=self.client.get('/api/genders/')
        data=r.json()
        assert len(data)==9

        assert gender_id_to_delete not in [i['id'] for i in data]
    def test_update_gender(self):
        genders=baker.make("Gender",10)
        gender: Gender=genders[2]

        r=self.client.get(f'/api/genders/{gender.id}/')
        data=r.json()
        assert data['name'] == gender.name

        r=self.client.put(f'/api/genders/{gender.id}/',{
            "name": "Мужской"
        },
        content_type='application/json')
        assert r.status_code==200

        r=self.client.get(f'/api/genders/{gender.id}/')
        data=r.json()
        assert data['name'] == "Мужской"

        gender.refresh_from_db()
        assert data['name']==gender.name
class ActorViewsetTestCase(TestCase):
    def test_get_list_actor(self):
        actor=baker.make("Actor")

        r=self.client.get('/api/actors/')
        data=r.json()
        print(data)
        assert actor.name==data[0]['name']
        assert actor.id==data[0]['id']
        assert len(data)==1
    def test_create_actor(self):
        r= self.client.post("/api/actors/",{
            "name": "actor"
        })

        new_actor_id=r.json()['id']

        actors=Actor.objects.all()
        assert len(actors) == 1
        new_actor=Actor.objects.filter(id=new_actor_id).first()
        assert new_actor.name == "actor"
    def test_delete_actor(self):
        actors=baker.make("Actor",10)
        r=self.client.get('/api/actors/')
        data=r.json()
        assert len(data)==10

        actor_id_to_delete=actors[3].id
        self.client.delete(f'/api/actors/{actor_id_to_delete}/')

        r=self.client.get('/api/actors/')
        data=r.json()
        assert len(data)==9

        assert actor_id_to_delete not in [i['id'] for i in data]
    def test_update_actor(self):
        actors=baker.make("Actor",10)
        actor: Actor=actors[2]

        r=self.client.get(f'/api/actors/{actor.id}/')
        data=r.json()
        assert data['name'] == actor.name

        r=self.client.put(f'/api/actors/{actor.id}/',{
            "name": "Совунья"
        },
        content_type='application/json')
        assert r.status_code==200

        r=self.client.get(f'/api/actors/{actor.id}/')
        data=r.json()
        assert data['name'] == "Совунья"

        actor.refresh_from_db()
        assert data['name']==actor.name
class AgeViewsetTestCase(TestCase):
    def test_get_list_age(self):
        age=baker.make("Age")

        r=self.client.get('/api/ages/')
        data=r.json()
        print(data)
        assert age.name==data[0]['name']
        assert age.id==data[0]['id']
        assert len(data)==1
    def test_create_age(self):
        r= self.client.post("/api/ages/",{
            "name": "age"
        })

        new_age_id=r.json()['id']

        ages=Age.objects.all()
        assert len(ages) == 1
        new_age=Age.objects.filter(id=new_age_id).first()
        assert new_age.name == "age"
    def test_delete_age(self):
        ages=baker.make("Age",10)
        r=self.client.get('/api/ages/')
        data=r.json()
        assert len(data)==10

        age_id_to_delete=ages[3].id
        self.client.delete(f'/api/ages/{age_id_to_delete}/')

        r=self.client.get('/api/ages/')
        data=r.json()
        assert len(data)==9

        assert age_id_to_delete not in [i['id'] for i in data]
    def test_update_age(self):
        ages=baker.make("Age",10)
        age: Age=ages[2]

        r=self.client.get(f'/api/ages/{age.id}/')
        data=r.json()
        assert data['name'] == age.name

        r=self.client.put(f'/api/ages/{age.id}/',{
            "name": "Совунья"
        },
        content_type='application/json')
        assert r.status_code==200

        r=self.client.get(f'/api/ages/{age.id}/')
        data=r.json()
        assert data['name'] == "Совунья"

        age.refresh_from_db()
        assert data['name']==age.name
class TypeViewsetTestCase(TestCase):
    def test_get_list_type(self):
        type=baker.make("Type")

        r=self.client.get('/api/types/')
        data=r.json()
        print(data)
        assert type.name==data[0]['name']
        assert type.id==data[0]['id']
        assert len(data)==1
    def test_create_type(self):
        r= self.client.post("/api/types/",{
            "name": "type"
        })

        new_type_id=r.json()['id']

        types=Type.objects.all()
        assert len(types) == 1
        new_type=Type.objects.filter(id=new_type_id).first()
        assert new_type.name == "type"
    def test_delete_type(self):
        types=baker.make("Type",10)
        r=self.client.get('/api/types/')
        data=r.json()
        assert len(data)==10

        type_id_to_delete=types[3].id
        self.client.delete(f'/api/types/{type_id_to_delete}/')

        r=self.client.get('/api/types/')
        data=r.json()
        assert len(data)==9

        assert type_id_to_delete not in [i['id'] for i in data]
    def test_update_type(self):
        types=baker.make("Type",10)
        type: Type=types[2]

        r=self.client.get(f'/api/types/{type.id}/')
        data=r.json()
        assert data['name'] == type.name

        r=self.client.put(f'/api/types/{type.id}/',{
            "name": "Совунья"
        },
        content_type='application/json')
        assert r.status_code==200

        r=self.client.get(f'/api/types/{type.id}/')
        data=r.json()
        assert data['name'] == "Совунья"

        type.refresh_from_db()
        assert data['name']==type.name