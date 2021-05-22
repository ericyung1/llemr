function defineOverviewFields(props) {
  const overviewFields = ["actionitem_status"];
  if (props.displayReferrals) {
    overviewFields.push("referral_status");
    overviewFields.push("referrals");
  }
  if (props.displayCaseManagers) {
    overviewFields.push("case_managers");
  }
  overviewFields.push("status");
  return overviewFields;
}

export default defineOverviewFields;
