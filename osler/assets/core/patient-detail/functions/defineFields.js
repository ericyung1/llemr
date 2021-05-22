function defineFields(data) {
  const fields = {
    id: {
      name: "ID",
      value: data.id,
    },
    name: {
      name: "Name",
      value: data.name,
    },
    latest_workup: {
      name: "Latest Workup",
      value: data.latest_workup, //will need to edit this
    },
    gender: {
      name: "Gender",
      value: data.gender.toLowerCase(),
    },
    age: {
      name: "Age",
      value: data.age,
    },
    status: {
      name: "Status",
      value: data.status,
    },
    case_managers: {
      name: "Case Managers",
      value: "NOT IMPLEMENETED IN API YET",
    },
    ethnicities: {
      name: "Ethnicity",
      value: data.ethnicities.join(", "),
    },
    actionitem_status: {
      name: "Action Items",
      value: data.actionitem_status,
    },
    referral_status: {
      name: "FQHC Referral Status",
      value: "NOT IMPLEMENTED IN API YET",
    },
    referrals: {
      name: "Referrals",
      value: "NOT IMPLEMENTED IN API YET",
    },
    update_url: {
      name: "Update URL",
      value: data.update_url,
    },
    new_note_url: {
      name: "New Note URL",
      value: data.new_note_url,
      label: "Write Note",
    },
    new_referral_url: {
      name: "New Referral URL",
      value: data.new_referral_url,
      label: "Make Referral",
    },
    make_appointment_url: {
      name: "Make Appointment URL",
      value: data.make_appointment_url,
      label: "Make Appointment",
    },
    give_vaccine_url: {
      name: "Give Vaccine URL",
      value: data.give_vaccine_url,
      label: "Give Vaccine",
    },
    upload_document_url: {
      name: "Upload Document URL",
      value: data.upload_document_url,
      label: "Upload Document",
    },
    view_labs_url: {
      name: "View Labs URL",
      value: data.view_labs_url,
      label: "View Labs",
    },
    languages: {
      name: "Languages",
      value: data.languages.join(", "),
    },
    date_of_birth: {
      name: "Date of Birth",
      value: data.date_of_birth,
    },
    email: {
      name: "Email",
      value: data.email || "Not Provided",
    },
    address: {
      name: "Address",
      value: data.address,
    },
    city: {
      name: "City",
      value: data.city,
    },
    state: {
      name: "State",
      value: data.state,
    },
    zip_code: {
      name: "Zip Code",
      value: data.zip_code,
    },
    all_phones: {
      name: "All Phones",
      value: data.all_phones,
    },
  };

  return fields;
}

export default defineFields;
