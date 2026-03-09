import { useState, useEffect } from 'react';
import StatusPill from './StatusPill';
import Notes from './Notes';
import Followups from './Followups';
import styles from './DetailDrawer.module.css';

const STATUSES = ['Applied', 'HR Screening', 'Interview', 'Offer', 'On Hold', 'Rejected'];

export default function DetailDrawer({ app, onClose, onStatusChange, onRefresh }) {
  const [status, setStatus] = useState(app?.status || 'Applied');

  useEffect(() => {
    if (app) setStatus(app.status);
  }, [app]);

  const handleStatusChange = async (val) => {
    setStatus(val);
    await onStatusChange(app.id, val);
    if (val === 'Rejected') { onClose(); return; }
    onRefresh();
  };

  if (!app) return null;

  return (
    <>
      <div className={`${styles.backdrop} ${app ? styles.open : ''}`} onClick={onClose} />
      <div className={`${styles.drawer} ${app ? styles.open : ''}`}>

        <div className={styles.header}>
          <div className={styles.headerInfo}>
            <div className={styles.company}>{app.company}</div>
            <div className={styles.role}>{app.role}</div>
            <div className={styles.pillWrap}><StatusPill status={status} /></div>
          </div>
          <button className={styles.closeBtn} onClick={onClose}>✕</button>
        </div>

        <div className={styles.body}>

          {/* STATUS */}
          <div className={styles.section}>
            <h4 className={styles.sectionTitle}>Update Status</h4>
            <select
              className={styles.statusSelect}
              value={status}
              onChange={e => handleStatusChange(e.target.value)}
            >
              {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          {/* TIMELINE */}
          <div className={styles.section}>
            <h4 className={styles.sectionTitle}>Timeline</h4>
            <div className={styles.timeline}>
              <div className={styles.tlItem}>
                <div className={styles.tlLabel}>Applied</div>
                <div className={styles.tlDate}>{app.applied_date}</div>
              </div>
              {status !== 'Applied' && (
                <div className={styles.tlItem}>
                  <div className={styles.tlLabel}>{status}</div>
                  <div className={styles.tlDate}>current stage</div>
                </div>
              )}
            </div>
          </div>

          {/* NOTES */}
          <div className={styles.section}>
            <h4 className={styles.sectionTitle}>Notes</h4>
            <Notes appId={app.id} />
          </div>

          {/* FOLLOWUPS */}
          <div className={styles.section}>
            <h4 className={styles.sectionTitle}>Follow-up Reminders</h4>
            <Followups appId={app.id} />
          </div>

        </div>
      </div>
    </>
  );
}
