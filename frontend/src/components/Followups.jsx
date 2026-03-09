import { useEffect, useState } from 'react';
import { getFollowups, addFollowup, markFollowupSent } from '../api/api';
import styles from './Followups.module.css';

export default function Followups({ appId }) {
  const [followups, setFollowups] = useState([]);
  const [date, setDate]           = useState('');
  const [loading, setLoading]     = useState(false);

  const load = () => {
    getFollowups(appId)
      .then(res => setFollowups(res.data))
      .catch(console.error);
  };

  useEffect(() => { load(); }, [appId]);

  const handleAdd = async () => {
    if (!date) return;
    setLoading(true);
    try {
      await addFollowup(appId, { followup_date: date });
      setDate('');
      load();
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };

  const handleSent = async (id) => {
    await markFollowupSent(id);
    load();
  };

  return (
    <div className={styles.wrapper}>
      {followups.length === 0 && (
        <p className={styles.empty}>No follow-ups scheduled.</p>
      )}
      {followups.map(f => (
        <div key={f.id} className={`${styles.item} ${f.sent ? styles.sent : ''}`}>
          <span className={styles.calIcon}>📅</span>
          <span className={styles.fDate}>{f.followup_date}</span>
          {f.sent
            ? <span className={styles.sentBadge}>✓ Sent</span>
            : <button className={styles.markBtn} onClick={() => handleSent(f.id)}>Mark Sent</button>
          }
        </div>
      ))}

      <div className={styles.addRow}>
        <input
          type="date"
          className={styles.dateInput}
          value={date}
          onChange={e => setDate(e.target.value)}
        />
        <button className={styles.btn} onClick={handleAdd} disabled={loading || !date}>
          {loading ? '…' : 'Schedule'}
        </button>
      </div>
    </div>
  );
}
