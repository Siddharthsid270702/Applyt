import { useState } from 'react';
import styles from './ApplicationForm.module.css';

const STATUSES = ['Applied', 'HR Screening', 'Interview', 'Offer', 'On Hold'];

export default function ApplicationForm({ onCreated }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    company: '', role: '', status: 'Applied', source: '',
    applied_date: new Date().toISOString().split('T')[0],
  });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async () => {
    setError('');
    if (!form.company.trim() || !form.role.trim()) {
      setError('Company and Role are required.');
      return;
    }
    setLoading(true);
    try {
      const payload = {
        company: form.company,
        role: form.role,
        status: form.status,
        source: form.source || null,
        applied_date: form.applied_date || undefined,
      };
      // import createApplication from api.js in actual usage
      const { createApplication } = await import('../api/api');
      await createApplication(payload);
      setForm({ company: '', role: '', status: 'Applied', source: '', applied_date: new Date().toISOString().split('T')[0] });
      setOpen(false);
      onCreated();
    } catch (err) {
      console.error(err);
      setError('Failed to create application. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button className={styles.btnAdd} onClick={() => setOpen(true)}>
        ＋ Add Application
      </button>

      {open && (
        <div className={styles.overlay} onClick={() => setOpen(false)}>
          <div className={styles.modal} onClick={e => e.stopPropagation()}>
            <h3 className={styles.modalTitle}>✦ Add New Application</h3>
            <p className={styles.modalSub}>Track your next opportunity in APPLYT</p>

            {error && <p className={styles.error}>{error}</p>}

            <div className={styles.formGrid}>
              <div className={styles.field}>
                <label className={styles.label}>Company</label>
                <input className={styles.input} name="company" placeholder="e.g. Google" value={form.company} onChange={handleChange} />
              </div>
              <div className={styles.field}>
                <label className={styles.label}>Role</label>
                <input className={styles.input} name="role" placeholder="e.g. SWE Intern" value={form.role} onChange={handleChange} />
              </div>
              <div className={styles.field}>
                <label className={styles.label}>Source</label>
                <input className={styles.input} name="source" placeholder="LinkedIn, Naukri…" value={form.source} onChange={handleChange} />
              </div>
              <div className={styles.field}>
                <label className={styles.label}>Applied Date</label>
                <input className={styles.input} type="date" name="applied_date" value={form.applied_date} onChange={handleChange} />
              </div>
              <div className={`${styles.field} ${styles.full}`}>
                <label className={styles.label}>Status</label>
                <select className={styles.input} name="status" value={form.status} onChange={handleChange}>
                  {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>

            <div className={styles.modalFooter}>
              <button className={styles.btnGhost} onClick={() => setOpen(false)}>Cancel</button>
              <button className={styles.btnPrimary} onClick={handleSubmit} disabled={loading}>
                {loading ? 'Adding…' : 'Add Application'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
