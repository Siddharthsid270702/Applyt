import axios from "axios";
import { auth } from "../firebase";

// ✅ Use Vite env variable for backend URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});

// ── Attach Firebase ID token to every request ────────────────────────────────
api.interceptors.request.use(async (config) => {
  const user = auth.currentUser;
  if (user) {
    const token = await user.getIdToken();
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// =======================
// APPLICATIONS
// =======================
export const getApplications     = ()           => api.get("/applications");
export const createApplication   = (data)       => api.post("/applications", data);
export const updateApplication   = (id, data)   => api.put(`/applications/${id}`, data);
export const deleteApplication   = (id)         => api.delete(`/applications/${id}`);

// =======================
// ARCHIVED
// =======================
export const getArchivedApplications = ()   => api.get("/applications/archived");
export const restoreApplication      = (id) => api.post(`/applications/archived/${id}/restore`);

// =======================
// NOTES
// =======================
export const getNotes  = (appId)       => api.get(`/applications/${appId}/notes`);
export const addNote   = (appId, data) => api.post(`/applications/${appId}/notes`, data);

// =======================
// FOLLOW UPS
// =======================
export const getFollowups      = (appId)         => api.get(`/applications/${appId}/followups`);
export const addFollowup       = (appId, data)   => api.post(`/applications/${appId}/followups`, data);
export const markFollowupSent  = (followupId)    => api.put(`/applications/followups/${followupId}/sent`);

export default api;
