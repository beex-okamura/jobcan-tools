export interface JobCanPunchResponse {
  result: number;
  state: number;
  current_status: string;
}

export interface ScrapingPayload {
  channel: string;
  jobcan_user_id: string;
  jobcan_password: string;
  zac_tenant_id: string;
  zac_login_id: string;
  zac_password: string;
  choice_work_type: string;
}
