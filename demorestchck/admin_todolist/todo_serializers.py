from rest_framework import serializers

from database.models import TodoList

# from collections import OrderedDict
# from django.utils.encoding import escape_uri_path
from django.core.exceptions import ValidationError
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import json
#from .serializers import ValidationError
import cgi

# #*************************************************************************************
# # TodoLists
# #*************************************************************************************
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = (
            'todo_list_guid',
            'todo_list_title',
            'todo_list_desc',
            'program_type_guid',
            'todo_list_json'
        )
    #def to_representation(self, instance):
    #    ret = super(TodoListSerializer, self).to_representation(instance)
    #    ret['todo_list_json'] = json.loads(ret['todo_list_json'])
    #    return ret


class TodoListUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoList
        fields = (
            'todo_list_guid',
            'todo_list_title',
            'todo_list_desc',
            'program_type_guid',
            'todo_list_json',
        )
        read_only_fields = ('todo_list_guid',)


    def create(self, validated_data):
        print "create function VALIDATED DATA:", validated_data

        try:
            newtodolist = TodoList.objects.create(**validated_data)
            print "TODOLIST CREATED:", newtodolist
            print("CREATED TODOLIST WITH GUID:", newtodolist.todo_list_guid)

            newtodolist.save()
            print "AFTER SAVE"
            return newtodolist
        except ValidationError: # it's a django Validataion Error
            print("ERROR CREATING TODOLIST IN SERIALIZER")
            #raise serializers.ValidationError("Error Creating New User")

    def update(self, instance, validated_data):
        """
        Update and return an existing `TodoList` instance, given the validated data.
        """
        print "VALIDATED DATA:", validated_data
        print "INSTANCE:", instance
        print "INSTANCE TODOLIST GUID IN UPDATE: ", validated_data.get('todo_list_guid', instance.todo_list_guid)


        instance.todo_list_title = validated_data.get('todo_list_title', instance.todo_list_title)
        instance.todo_list_desc = validated_data.get('todo_list_desc', instance.todo_list_desc)
        instance.program_type_guid = validated_data.get('program_type_guid', instance.program_type_guid)
        instance.todo_list_json = validated_data.get('todo_list_json', instance.todo_list_json)

        instance.save()
        return instance

    #def to_representation(self, instance):
    #    ret = super(TodoListUpdateSerializer, self).to_representation(instance)
    #    ret['todo_list_json'] = json.loads(ret['todo_list_json'])
    #    return ret

"""
# #*************************************************************************************
# # User Status
# #*************************************************************************************
class AuthUserStatusSadcSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUserStatusSadc
        fields = (
            'auth_user_status_sadc_desc',
        )
# #*************************************************************************************
# # Contact Type
# #*************************************************************************************
class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = (
            'contact_type_desc',
        )
# #*************************************************************************************
# # Person Type ( Org Type )
# #*************************************************************************************
class PersonTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonType
        fields = (
            'person_type_desc',
        )
# #*************************************************************************************
# # Roles
# #*************************************************************************************
class AuthRoleSadcSerializer(serializers.ModelSerializer):
    #auth_role_guid = serializers.IntegerField()
    auth_role_guid = serializers.CharField(max_length=36)
    class Meta:
        model = AuthRoleSadc
        fields = (
            'auth_role_guid',
            'auth_role_name',
            'description',
            'admin_managed',
            'county_code',
            'muni_code',
            'tier_desc',
            'tier_group_desc',
            'tier_subgroup_desc',
            'partner_guid'
        )
# #*************************************************************************************
# # Roles with limited information
# #*************************************************************************************

class AuthRoleSadcSerializerLimited(serializers.ModelSerializer):
    #auth_role_guid = serializers.IntegerField()
    auth_role_guid = serializers.CharField(max_length=36)
    class Meta:
        model = AuthRoleSadc
        fields = (
            'auth_role_guid',
            'auth_role_name',
        )
# #*************************************************************************************
# # Users
# #*************************************************************************************
class AuthUserSadcSerializer(serializers.ModelSerializer):
    role = AuthRoleSadcSerializerLimited(many=True)  # We just want role guid
    class Meta:
        model = AuthUserSadc
        fields = (
            'auth_user_guid',
            'salutation',
            'first_name',
            'last_name',
            'title',
            'organization',
            'address',
            'city',
            'state',
            'zip',
            'zip4',
            'email_primary',
            'email_alternate',
            'phone_primary',
            'phone_primary_ext',
            'phone_alternate',
            'phone_alternate_ext',
            'auth_user_status_desc',
            'contact_type_desc',
            'person_type_desc',
            'role',
        )
        read_only_fields = ('auth_user_guid',)

    def create(self, validated_data):
        print "create function VALIDATED DATA:", validated_data
        #role_data = validated_data['role']
        popped_role_data = validated_data.pop('role')
        print "ROLE_DATA_KEYS", popped_role_data
        print "AFTER VALIDATED DATA: "
        # Get non text values off of the validated data
        popped_contact_type_desc = validated_data.pop('contact_type_desc')
        popped_auth_user_status_desc = validated_data.pop('auth_user_status_desc')
        popped_person_type = validated_data.pop('person_type_desc')
        print validated_data
        # Escape the data and remove leading trailing spaces
        for vkey in validated_data:
            print "KEY OF VALIDATED:", vkey
            validated_data[vkey] = cgi.escape(validated_data[vkey]).lstrip().rstrip()
        print("ESCAPED DATA:", validated_data)
        # Add non text values back in
        validated_data['contact_type_desc'] = popped_contact_type_desc
        validated_data['auth_user_status_desc'] = popped_auth_user_status_desc
        validated_data['person_type_desc'] = popped_person_type
        # Create the user without roles
        # When creating a new user, lots of things can go wrong since it is also creating an ArcGIS server user and
        # adding it to a role.  If any of that fails, we must invalidate the serializer.
        try:
            user = AuthUserSadc.objects.create(**validated_data)
            print "USER CREATED:", user
            print("CREATED USER WITH GUID:", user.auth_user_guid)
            print "LENGTH OF ROLE_DATA", len(popped_role_data)
            role_list = []
            for role in popped_role_data:
                auth_role_guid = role.get('auth_role_guid')
                try:
                    print"THE ROLE GUID IS:", auth_role_guid
                    the_role = AuthRoleSadc.objects.get(pk=auth_role_guid)
                    print "ROLE:", the_role
                except AuthRoleSadc.DoesNotExist:
                    print "THROWING EXCEPTION FOR ROLE NOT FOUND"
                    raise serializers.ValidationError("Invalid role.")
                ur = WxUserRole(auth_user_guid=user, auth_role_guid=the_role)
                ur.save()
            print "AFTER LOOP"
            user.save()
            print "AFTER SAVE"
            return user
        except ValidationError: # it's a django Validataion Error
            print("ERROR CREATING USER IN SERIALIZER")
            raise serializers.ValidationError("Error Creating New User")

    def update(self, instance, validated_data):

        #Update and return an existing `AuthUser` instance, given the validated data.

        #instance.username = validated_data.get('username', instance.username)
        print "VALIDATED DATA:", validated_data
        print "INSTANCE:", instance
        print "INSTANCE ORG IN UPDATE: ", validated_data.get('organization', instance.organization)
        print "INSTANCE USER GUID IN UPDATE: ", validated_data.get('auth_user_guid', instance.auth_user_guid)
        # Check the foreign key values to make sure they resolve to actual records
        # TODO:   instance values are object types..  The next check might not be needed.
        print "UPDATE: USER STATUS:",validated_data.get('auth_user_status_desc', instance.auth_user_status_desc)
        print "UPDATE: USER CONTACT TYPE:",validated_data.get('contact_type_desc', instance.contact_type_desc)
        print "UPDATE: USER PERSON TYPE:",validated_data.get('person_type_desc', instance.person_type_desc)
        # Roles come in as an ordered dictionary.  Must translate to plain list
        role_ord_dict = validated_data.get('role', instance.role)
        print "NUMBER OF ROLES:", len(role_ord_dict)
        instance.role.clear()
        for role in role_ord_dict:
            auth_role_guid = role.get('auth_role_guid')
            try:
                print"THE ROLE GUID IS:", auth_role_guid
                the_role = AuthRoleSadc.objects.get(pk=auth_role_guid)
                print "ROLE:", the_role
            except AuthRoleSadc.DoesNotExist:
                print "THROWING EXCEPTION FOR ROLE NOT FOUND"
                raise serializers.ValidationError("Invalid role.")
            print("CREATING USER/ROLE ENTRY:")
            ur = WxUserRole(auth_user_guid=instance, auth_role_guid=the_role)
            ur.save()
            print("CREATED THE USER/ROLE ENTRY:")
        instance.salutation = validated_data.get('salutation', instance.salutation)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.title = validated_data.get('title', instance.title)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.zip = validated_data.get('zip', instance.zip)
        instance.zip4 = validated_data.get('zip4', instance.zip4)
        instance.email_primary = validated_data.get('email_primary', instance.email_primary)
        instance.email_alternate = validated_data.get('email_alternate', instance.email_alternate)
        instance.phone_primary = validated_data.get('phone_primary', instance.phone_primary)
        instance.phone_primary_ext = validated_data.get('phone_primary_ext', instance.phone_primary_ext)
        instance.phone_alternate = validated_data.get('phone_alternate', instance.phone_alternate)
        instance.phone_alternate_ext = validated_data.get('phone_alternate_ext', instance.phone_alternate_ext)
        instance.auth_user_status_desc = validated_data.get('auth_user_status_desc', instance.auth_user_status_desc)
        instance.contact_type_desc = validated_data.get('contact_type_desc', instance.contact_type_desc)
        instance.person_type_desc = validated_data.get('person_type_desc', instance.person_type_desc)
        instance.save()
        return instance
# ######################################################################################################################
# # Partner Type for Roles
# ######################################################################################################################
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = (
            'partner_guid',
            'partner_name',
            'active_flg',
            'partner_type_desc',
            'county_code',
            'muni_code'
        )

# ######################################################################################################################
# # Tier for Roles
# ######################################################################################################################
class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = (
            'tier_desc',
        )
# ######################################################################################################################
# # Group for Roles
# ######################################################################################################################
class TierGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TierGroup
        fields = (
            'tier_group_desc',
        )
#
# ######################################################################################################################
# # Sub-Group for Roles
# ######################################################################################################################
class TierSubgroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TierSubgroup
        fields = (
            'tier_subgroup_desc',
        )
# ######################################################################################################################
# # Counties for Roles
# ######################################################################################################################
class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = (
            'county_code',
            'county_name',
            'county_label',
            'gnis_name',
            'gnis'

        )
# ######################################################################################################################
# # Municipality for Roles
# ######################################################################################################################
class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = (
            'muni_code',
            'name',
            'gnis_name',
            'gnis',
            'county'
        )
"""