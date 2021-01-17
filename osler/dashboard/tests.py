# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import range
import datetime
from django.utils.timezone import now

from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings

from osler.core.models import (Gender, Patient, ContactMethod, Encounter, EncounterStatus)

from osler.workup.models import Workup

from osler.core.tests.test_views import log_in_user, build_user
from osler.users.tests import factories as user_factories
from osler.core.tests import factories as core_factories


def dewhitespace(s):
    return "".join(s.split())


class TestAttendingDashboard(TestCase):

    fixtures = ['core', 'workup']

    def setUp(self):

        # build an attending and a clinical student
        self.attending = build_user([user_factories.AttendingGroupFactory])
        self.clinical_student = build_user()
        log_in_user(self.client, self.attending)

        self.wu_info = dict(
            chief_complaint="SOB", diagnosis="MI", hpi="A", pmh="B", psh="W",
            meds="C", allergies="D", fam_hx="E", soc_hx="F", ros="", pe="",
            a_and_p="")

        # prepare a patient with an unsigned wu today, in addition to
        # what comes in in the fixture

        self.pt2 = Patient.objects.create(
            first_name="Arthur", last_name="Miller", middle_name="",
            phone='+49 178 236 5288', gender=Gender.objects.first(),
            address='Schulstrasse 9', city='Munich', state='BA',
            zip_code='63108', pcp_preferred_zip='63018',
            date_of_birth=datetime.date(1994, 1, 22),
            patient_comfortable_with_english=False,
            preferred_contact_method=ContactMethod.objects.first(),
        )

        EncounterStatus.objects.create(name="Active",is_active=True)

        self.encounter_info = dict(
            clinic_day=now().date(),
            status=EncounterStatus.objects.first())

        Encounter.objects.create(patient=Patient.objects.first(), **self.encounter_info)

        self.wu2 = Workup.objects.create(
            encounter=Encounter.objects.create(
                patient=self.pt2,
                **self.encounter_info),
            author=self.clinical_student,
            author_type=self.clinical_student.groups.first(),
            patient=self.pt2,
            **self.wu_info)

    def test_pt_without_note(self):
        response = self.client.get(reverse('dashboard-attending'))

        #since there is 1 pt without a workup loaded in fixtures/core
        self.assertEqual(
            len(response.context['no_note_patients']),
            1)
        self.assertEqual(
            response.context['no_note_patients'][0],
            Patient.objects.first())

    def test_pt_without_note_and_pt_unsigned(self):

        # assign wu2 to our attending
        self.wu2.attending = self.attending
        self.wu2.save()

        # prepare a patient with an unsigned wu today, NOT assigned to
        # our attending
        pt3 = Patient.objects.create(
            first_name="John", last_name="Doe", middle_name="",
            phone='454545', gender=Gender.objects.first(),
            address='A', city='B', state='C',
            zip_code='12345', pcp_preferred_zip='12345',
            date_of_birth=datetime.date(1992, 4, 22),
            patient_comfortable_with_english=False,
            preferred_contact_method=ContactMethod.objects.first(),
        )
        wu3 = Workup.objects.create(
            encounter=Encounter.objects.create(
                patient=pt3,
                **self.encounter_info),
            author=self.clinical_student,
            author_type=self.clinical_student.groups.first(),
            patient=pt3,
            **self.wu_info)

        response = self.client.get(reverse('dashboard-attending'))

        # we should have one no note patient
        self.assertEqual(
            len(response.context['no_note_patients']),
            1)
        self.assertEqual(
            response.context['no_note_patients'][0],
            Patient.objects.get(pk=1))

        # and one encounter with workup assigned to our attending
        self.assertEqual(len(response.context['clinics']), 1)
        # with one patient
        self.assertContains(response, reverse('core:patient-detail',
                                              args=(self.pt2.pk,)))
        # which is marked as unattested
        self.assertContains(response, '<tr  class="warning" >', count=1)

        wu3.attending = self.attending
        wu3.sign(self.attending, self.attending.groups.first())
        wu3.save()

        response = self.client.get(reverse('dashboard-attending'))

        # now two encounters with workup assigned to our attending
        self.assertEqual(len(response.context['clinics']), 2)
        # with two patients
        self.assertContains(response, reverse('core:patient-detail',
                                              args=(self.pt2.pk,)))
        self.assertContains(response, reverse('core:patient-detail',
                                              args=(pt3.pk,)))
        # ONE of which are marked as unattested
        self.assertContains(response, '<tr  class="warning" >', count=1)

    @override_settings(OSLER_CLINIC_DAYS_PER_PAGE=3)
    def test_dashboard_pagination(self):
        response = self.client.get(reverse('dashboard-attending'))

        # since we're on the first page, the "back" pagination button
        # should be disabled
        self.assertIn(
            dewhitespace('''
                <li class="disabled"><a aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a></li>'''),
            dewhitespace(response.content.decode('utf-8')))
        # since there's only one page, the "forward" pagination button
        # should be disabled
        self.assertIn(
            dewhitespace('''
                <li class="disabled"> <a aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a> </li>'''),
            dewhitespace(response.content.decode('utf-8')))

        # since there's only one page, only one page marker should be shown
        self.assertContains(
            response, '<a href="?page=', count=1)

        for i in range(5):
            pt = Patient.objects.create(
                first_name="John", last_name="Doe", middle_name="",
                phone='454545', gender=Gender.objects.first(),
                address='A', city='B', state='C',
                zip_code='12345', pcp_preferred_zip='12345',
                date_of_birth=datetime.date(1992, i + 3, 22),
                patient_comfortable_with_english=False,
                preferred_contact_method=ContactMethod.objects.first(),
            )
            e = Encounter.objects.create(
                clinic_day=datetime.date(2001, i + 1, 1),
                patient=pt,
                status=EncounterStatus.objects.first(),)
            Workup.objects.create(
                attending=self.attending,
                encounter=e,
                author=self.clinical_student,
                author_type=self.clinical_student.groups.first(),
                patient=pt,
                **self.wu_info)

        response = self.client.get(reverse('dashboard-attending'))

        # now we should have two pages
        self.assertContains(
            response, '<a href="?page=', count=2)
        # since we're on the first page, the "back" pagination button
        # should still be disabled
        self.assertIn(
            dewhitespace('''
                <li class="disabled"><a aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a></li>'''),
            dewhitespace(response.content.decode('utf-8')))
        # since there's only one page, the "forward" pagination button
        # should be disabled
        self.assertIn(
            dewhitespace('''
              <li><a href="?page=2" aria-label="Next">
                <span aria-hidden="true">&raquo;</span>
              </a></li>'''),
            dewhitespace(response.content.decode('utf-8')))

    @override_settings(OSLER_CLINIC_DAYS_PER_PAGE=3)
    def test_dashboard_page_out_of_range(self):

        for i in range(10):
            pt = Patient.objects.create(
                first_name="John", last_name="Doe", middle_name="",
                phone='454545', gender=Gender.objects.first(),
                address='A', city='B', state='C',
                zip_code='12345', pcp_preferred_zip='12345',
                date_of_birth=datetime.date(1992, i + 1, 22),
                patient_comfortable_with_english=False,
                preferred_contact_method=ContactMethod.objects.first(),
            )
            e = Encounter.objects.create(patient=pt, **self.encounter_info)
            Workup.objects.create(
                attending=self.attending,
                encounter=e,
                author=self.clinical_student,
                author_type=self.clinical_student.groups.first(),
                patient=pt,
                **self.wu_info)

        response = self.client.get(reverse('dashboard-attending') +
                                   '?page=99')

        #Making 10 encounters with 3 per page, should make 4 pages
        #So the previous button should go towards the page before
        n_pages = (Encounter.objects.count() //
                   settings.OSLER_CLINIC_DAYS_PER_PAGE)-1

        # since we're on the last page, the "back" pagination button
        # should be enabled (i.e. no 'class="disabled"')
        self.assertIn(
            dewhitespace('''
                <a href="?page=%s" aria-label="Previous">
                    <span aria-hidden="true">&laquo;
                ''' % n_pages),
            dewhitespace(response.content.decode('utf-8')))
        # since there's only one page, the "forward" pagination button
        # should be disabled
        self.assertIn(
            dewhitespace('''
                <li class="disabled"> <a aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a> </li>'''),
            dewhitespace(response.content.decode('utf-8')))


class TestActiveDashboard(TestCase):

    def setUp(self):
        self.coordinator = build_user([user_factories.CaseManagerGroupFactory])
        log_in_user(self.client, self.coordinator)

        self.pt1 = core_factories.PatientFactory()
        self.pt2 = core_factories.PatientFactory()
        self.pt3 = core_factories.PatientFactory()

        #pt1 has an active encounter today
        self.encounter1 = core_factories.EncounterFactory(patient=self.pt1)
        self.encounter1.order = 1
        #pt2 has an active encounter today
        self.encounter2 = core_factories.EncounterFactory(patient=self.pt2)
        self.encounter2.order = 2
        #pt3 has an inactive encounter today
        self.encounter3 = core_factories.EncounterFactory(patient=self.pt3,
            status=core_factories.EncounterStatusFactory(name="Nope",is_active=False))
        self.encounter3.order = 3

    def test_active_pts_reorder(self):
        response = self.client.get(reverse('dashboard-active'))
        #only 2 active patients
        assert len(response.context['object_list'])==2
        assert response.context['object_list'][0] == self.pt1
        
        self.encounter1.order = 2
        self.encounter1.save()
        self.encounter2.order = 1
        self.encounter2.save()

        #now pt2 should be first
        response = self.client.get(reverse('dashboard-active'))
        assert response.context['object_list'][0] == self.pt2
