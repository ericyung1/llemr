'''The datamodels for the Osler core'''
from itertools import chain

from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned

from simple_history.models import HistoricalRecords
from adminsortable.models import SortableMixin

from osler.core import validators
from osler.core import utils

from osler.users.utils import group_has_perm

class Language(models.Model):
    """A natural language, spoken by a provider or patient.
    """
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

    def __str__(self):
        return self.name

    def short_name(self):
        return self.name[0]


class ContactMethod(models.Model):
    '''Simple text-contiaining class for storing the method of contacting a
    patient for followup followed up with (i.e. phone, email, etc.)'''

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class ReferralType(models.Model):
    """The different kind of care availiable at a referral center."""

    name = models.CharField(max_length=100, primary_key=True)
    is_fqhc = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def slugify(self):
        return slugify(self.name)


class ReferralLocation(models.Model):
    """Location that we can refer to."""

    name = models.CharField(max_length=300)
    address = models.TextField()
    care_availiable = models.ManyToManyField(ReferralType)

    def __str__(self):
        if self.address:
            return self.name + " (" + self.address.splitlines()[0] + ")"
        else:
            return self.name


class Ethnicity(models.Model):
    """An ethnicity, of a patient.
    """

    class Meta:
        verbose_name_plural = "ethnicities"

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class ActionInstruction(models.Model):
    instruction = models.CharField(max_length=50, primary_key=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.instruction


class Outcome(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Person(models.Model):

    class Meta:
        abstract = True

    first_name = models.CharField(
        max_length=100, validators=[validators.validate_name])
    last_name = models.CharField(
        max_length=100, validators=[validators.validate_name])
    middle_name = models.CharField(
        max_length=100, blank=True, validators=[validators.validate_name])

    phone = models.CharField(max_length=40, null=True, blank=True)
    languages = models.ManyToManyField(
        Language, help_text="Specify here languages that are spoken at a "
                            "level sufficient to be used for medical "
                            "communication.")

    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)

    def name(self, reverse=True, middle_short=True):
        if self.middle_name:
            if middle_short:
                middle = "".join([mname[0] + "." for mname
                                  in self.middle_name.split()])
            else:
                middle = self.middle_name
        else:
            middle = ""

        if reverse:
            return " ".join([self.last_name + ",",
                             self.first_name,
                             middle])
        else:
            return " ".join([self.first_name,
                             middle,
                             self.last_name])


class Provider(Person):
    """Data additional to the User model to track about each provider.

    Primarily combines Person and User.
    """

    # Users should be made inactive rather than deleted in almost all cases
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return "Provider Object on %s." % self.user


class Patient(Person):

    class Meta:
        permissions = [
            ('case_manage_Patient', "Can act as a case manager."),
            ('activate_Patient', "Can in/activate patients")
        ]
        ordering = ["last_name",]


    case_managers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    outcome = models.ForeignKey(Outcome, null=True, blank=True,
                                on_delete=models.PROTECT)

    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=3)
    zip_code = models.CharField(max_length=5,
                                validators=[validators.validate_zip])
    country = models.CharField(max_length=100)

    pcp_preferred_zip = models.CharField(max_length=5,
                                         validators=[validators.validate_zip],
                                         blank=True,
                                         null=True)

    date_of_birth = models.DateField(
        help_text='MM/DD/YYYY',
        validators=[validators.validate_birth_date])

    patient_comfortable_with_english = models.BooleanField(default=True)

    ethnicities = models.ManyToManyField(Ethnicity)

    # Alternative phone numbers have up to 4 fields and each one is associated
    # with the person that owns phone

    # TODO: we should really come up with a better way of representing these
    # data

    alternate_phone_1_owner = models.CharField(max_length=40, blank=True, null=True)
    alternate_phone_1 = models.CharField(max_length=40, blank=True, null=True)

    alternate_phone_2_owner = models.CharField(max_length=40, blank=True, null=True)
    alternate_phone_2 = models.CharField(max_length=40, blank=True, null=True)

    alternate_phone_3_owner = models.CharField(max_length=40, blank=True, null=True)
    alternate_phone_3 = models.CharField(max_length=40, blank=True, null=True)

    alternate_phone_4_owner = models.CharField(max_length=40, blank=True, null=True)
    alternate_phone_4 = models.CharField(max_length=40, blank=True, null=True)

    preferred_contact_method = models.ForeignKey(
        ContactMethod, blank=True, null=True, on_delete=models.PROTECT)

    email = models.EmailField(blank=True, null=True)

    history = HistoricalRecords()

    def age(self):
        today = now().date()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def __str__(self):
        return self.name()

    def active_action_items(self):
        '''return a list of ActionItems that are 1) not done and
        2) due today or before. The list is sorted by due_date'''

        return sorted(
            ActionItem.objects.filter(patient=self.pk) \
                .filter(completion_author=None) \
                .filter(due_date__lte=now().date()),
            key=lambda ai: ai.due_date)

    def done_action_items(self):
        '''return the set of action items that are done, sorted
        by completion date'''

        return sorted(
            ActionItem.objects.filter(patient=self.pk)\
                .exclude(completion_author=None),
            key=lambda ai: ai.completion_date)

    def inactive_action_items(self):
        '''return a list of action items that aren't done, but aren't
        due yet either, sorted by due date.'''

        return sorted(
            ActionItem.objects.filter(patient=self.pk)\
                .filter(completion_author=None)\
                .filter(due_date__gt=now().date()),
            key=lambda ai: ai.due_date)

    def actionitem_status(self):
        # The active_action_items, done_action_items, and inactive_action_items
        # aren't a big deal to use when getting just one patient
        # For the all_patients page though (one of the pages that use status),
        # hitting the db three times per patient adds up.
        # Here, we only hit the db once by asking the db for all action items
        # for a patient, then sorting them in memory.

        # Combine action items with referral followup requests for status
        
        #TODO: Change this into OSLER_TODO_LIST_MANAGERS
        patient_action_items = self.actionitem_set.all()
        referral_followup_requests = self.followuprequest_set.all()
        vaccine_action_items = self.vaccineactionitem_set.all()
        patient_action_items = list(chain(patient_action_items,
                                          referral_followup_requests,
                                          vaccine_action_items))


        overdue = [ai for ai in patient_action_items if ai.due_date <= now().date() and ai.completion_author is None]
        if len(overdue) > 0:
            oldest = min(overdue, key=lambda k: k.due_date)
            time_delta = now().date() - oldest.due_date
            return f'{oldest.short_name()} {time_delta.days} days past due'

        pending = [ai for ai in patient_action_items if ai.due_date > now().date() and ai.completion_author is None]
        if len(pending) > 0:
            next_item = min(pending, key=lambda k: k.due_date)
            time_delta = next_item.due_date - now().date()
            return f'{next_item.short_name()} due in {time_delta.days} days'

        done = [ai for ai in patient_action_items if ai.completion_author is not None]

        if len(done) > 0:
            return "all actions complete"

        else:
            return "no pending actions"

    def followup_set(self):
        followups = []
        followups.extend(self.actionitemfollowup_set.all())

        return followups

    def pending_workup_set(self):
        return self.workup_set.filter(is_pending=True)
    
    def completed_workup_set(self):
        return self.workup_set.filter(is_pending=False)

    def latest_workup_helper(self, qs):
        try:
            return qs.all()[0]
        except IndexError:
            return None

    def latest_pending_workup(self):
        return self.latest_workup_helper(self.pending_workup_set())

    def latest_completed_workup(self):
        return self.latest_workup_helper(self.completed_workup_set())

    def latest_workup(self):
        return self.latest_workup_helper(self.workup_set)

    def notes(self):
        '''Returns a list of all the notes (workups and followups) associated
        with this patient ordered by date written.'''
        note_list = []

        note_list.extend(self.workup_set.all())
        note_list.extend(self.followup_set())
        note_list.extend(self.document_set.all())
        note_list.extend(self.vaccinedose_set.all())
        note_list.extend(self.vaccinefollowup_set.all())
        note_list.extend(self.patientcontact_set.all())
        note_list.extend(self.dispensehistory_set.all())

        return sorted(note_list, key=lambda k: k.written_datetime)

    def last_seen(self):
        latest_wu = self.latest_completed_workup()
        if latest_wu:
            return latest_wu.written_datetime
        else:
            # presumably if a patient doesn't have a last workup this is the first time they are being seen?
            return now().date()
    
    def all_phones(self):
        '''Returns a list of tuples of the form (phone, owner) of all the
        phones associated with this patient.'''

        phones = [(self.phone, '')]
        phones.extend([(getattr(self, 'alternate_phone_'+str(i)),
                        getattr(self, 'alternate_phone_'+str(i)+'_owner'))
                       for i in range(1, 5)])

        return phones

    def last_encounter(self):
        if Encounter.objects.filter(patient=self.pk).exists():
            last_encounter = Encounter.objects.filter(patient=self.pk).order_by('clinic_day').last()
            return last_encounter
        else:
            return None

    def status(self):
        if self.last_encounter() is not None:
            return self.last_encounter().status
        else:
            return default_inactive_status()

    def toggle_active_status(self, user, group):
        ''' Will Activate or Inactivate the Patient'''
        user_has_group = user.groups.filter(pk=group.pk).exists()
        if user_has_group and self.group_can_activate(group):
            #active encounter then inactivate
            if self.status().is_active:
                encounter = self.last_encounter()
                encounter.status = default_inactive_status()
                encounter.save()
            else:
                #no active encounter today, get today's encounter and activate or make new active
                try:
                    encounter, created = Encounter.objects.get_or_create(patient=self, clinic_day=now().date(),
                        defaults={'status': default_active_status()})
                    if not encounter.status.is_active:
                        encounter.status = default_active_status()
                        encounter.save()
                except MultipleObjectsReturned:
                    raise ValueError("Somehow there are multiple encounters for this patient and "
                        "clinc day. Please delete one in the admin panel or cry for help.")
        else:
            raise ValueError("Special permissions are required to change active status.")

    def detail_url(self):
        return reverse('core:patient-detail', args=(self.pk,))

    def update_url(self):
        return reverse('core:patient-update', args=(self.pk,))

    def activate_url(self):
        return reverse('core:patient-activate-home', args=(self.pk,))

    def new_note_url(self):
        return reverse('new-note-dispatch', args=(self.pk,))
    
    def new_referral_url(self):
        return reverse('select-referral-type', args=(self.pk,))

    def give_vaccine_url(self):
        return reverse('select-vaccine-series', args=(self.pk,))

    def upload_document_url(self):
        return reverse('core:new-document', args=(self.pk,))
    
    def view_labs_url(self):
        return reverse('all-labs-table', args=(self.pk,))

    def make_appointment_url(self):
        return reverse('appointment-new')+"?pt_id="+str(self.pk)

    def log_followup_url(self):
        return reverse('select-referral', args=(self.pk,))

    def new_ai_url(self):
        return reverse('core:new-action-item', args=(self.pk,))

    def demographics_create_url(self):
        return reverse('demographics-create', args=(self.pk,))

    @classmethod
    def group_can_activate(cls, group):
        """takes a group and checks if it has activate permission to this object."""
        return group_has_perm(group, 'core.activate_Patient')


class Note(models.Model):
    class Meta:
        abstract = True
        ordering = ["-written_datetime", "-last_modified"]

    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    author_type = models.ForeignKey(Group, on_delete=models.PROTECT)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)

    written_datetime = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class DocumentType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Document(Note):
    title = models.CharField(max_length=200)
    image = models.FileField(
        help_text="Please deidentify all file names before upload! "
                  "Delete all files after upload!",
        upload_to=utils.make_filepath,
        verbose_name="PDF File or Image Upload")
    comments = models.TextField()
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)

    history = HistoricalRecords()

    def short_text(self):
        return self.title


class CompletableManager(models.Manager):
    """ Class that handles queryset filers for Completable classes."""

    def get_active(self, patient):
        """ Returns all active elements of Completable class."""
        return self.get_queryset()\
            .filter(patient=patient)\
            .filter(completion_author=None)\
            .filter(due_date__lte=now().date())\
            .order_by('completion_date')

    def get_inactive(self, patient):
        """ Returns all inactive elements of Completable class."""
        return self.get_queryset()\
            .filter(patient=patient)\
            .filter(completion_author=None)\
            .filter(due_date__gt=now().date())\
            .order_by('completion_date')

    def get_completed(self, patient):
        """ Returns all completed elements of Completable class."""
        return self.get_queryset()\
            .filter(patient=patient)\
            .exclude(completion_author=None)\
            .order_by('completion_date')


class CompletableMixin(models.Model):
    """CompleteableMixin is for anything that goes in that list of
    stuff on the Patient detail page. They can be marked as
    complete.
    """

    class Meta:
        abstract = True

    objects = CompletableManager()

    completion_date = models.DateTimeField(blank=True, null=True)
    completion_author = models.ForeignKey(
        get_user_model(),
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_completed",
        on_delete=models.PROTECT)
    due_date = models.DateField(help_text="MM/DD/YYYY")

    def done(self):
        """Return true if this ActionItem has been marked as done."""
        return self.completion_date is not None

    def mark_done(self, user):
        self.completion_date = now()
        self.completion_author = user

    def clear_done(self):
        self.completion_author = None
        self.completion_date = None

    def short_name(self):
        """A short (one or two word) description of the action type that
        this completable represents.

        For example, ReferralFollowup has "Referral".
        """
        raise NotImplementedError(
            "All Completables must have an 'short_name' property that "
            "is indicates what one has to do of completable this is ")

    def summary(self):
        """Text that should be displayed on the core:patient-detail view to
        describe what must be done to mark this Completable as done.

        For example, this is the comments for of ActionItem.
        """
        raise NotImplementedError(
            "All Completables must have an 'summary' method that provides "
            "a summary of the action that must be undertaken.")


class AbstractActionItem(Note, CompletableMixin):
    '''Abstract class for completable tasks, inherit from this for app-specific tasks'''
    class Meta(object):
        abstract = True

    instruction = models.ForeignKey(ActionInstruction,
                                    on_delete=models.PROTECT)
    comments = models.TextField()

    def class_name(self):
        return self.__class__.__name__

    def short_name(self):
        return str(self.instruction)

    def summary(self):
        return self.comments

    def attribution(self):
        if self.done():
            return " ".join(["Marked done by", self.completion_author.name,
                             "on", str(self.completion_date.date())])
        else:
            return " ".join(["Added by", self.author.name, "on",
                             str(self.written_datetime.date())])


class ActionItem(AbstractActionItem):
    priority = models.BooleanField(
        default=False,
        help_text='Check this box if this action item is high priority')

    MARK_DONE_URL_NAME = 'done-action-item'

    history = HistoricalRecords()

    def mark_done_url(self):
        return reverse('core:%s' % self.MARK_DONE_URL_NAME, args=(self.id,))

    def admin_url(self):
        return reverse('admin:core_actionitem_change',
                       args=(self.id,))

    def __str__(self):
        return " ".join(["AI for", str(self.patient) + ":",
                         str(self.instruction), "due on", str(self.due_date)])


class EncounterStatus(models.Model):
    '''Different status for encounter, as simple as Active/Inactive 
    or Waiting/Team in Room/Attending etc'''
    name = models.CharField(max_length=100, primary_key=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


def default_active_status():
    status, created = EncounterStatus.objects.get_or_create(
        name=settings.OSLER_DEFAULT_ACTIVE_STATUS[0],
        is_active=settings.OSLER_DEFAULT_ACTIVE_STATUS[1])
    return status


def default_inactive_status():
    status, created = EncounterStatus.objects.get_or_create(
        name=settings.OSLER_DEFAULT_INACTIVE_STATUS[0],
        is_active=settings.OSLER_DEFAULT_INACTIVE_STATUS[1])
    return status


class Encounter(SortableMixin):
    '''Encounter for a given patient on a given clinic day
    Holds all associated notes, labs, etc performed on that clinic day
    Can reoder in admin panel for Active Patients page'''
    class Meta:
        ordering = ['order']
    
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    clinic_day = models.DateField()
    status = models.ForeignKey(EncounterStatus, on_delete=models.PROTECT)

    sorting_filters = (
        ('Active Encounters', {'status__is_active': True}),
        )

    def __str__(self):
        return str(self.patient) + " on " + self.clinic_day.strftime('%A, %B %d, %Y')
