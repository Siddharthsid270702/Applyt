import styles from './StatCards.module.css';

export default function StatCards({ apps }) {
  const total      = apps.length;
  const interviews = apps.filter(a => a.status === 'Interview').length;
  const offers     = apps.filter(a => a.status === 'Offer').length;
  const today      = new Date().toISOString().split('T')[0];
  const followupsDue = apps.reduce((acc, a) => {
    return acc + (a.followups || []).filter(f => !f.sent && f.followup_date <= today).length;
  }, 0);

  return (
    <div className={styles.grid}>
      <div className={`${styles.card} ${styles.teal}`}>
        <div className={styles.label}>Total Active</div>
        <div className={styles.value}>{total}</div>
        <div className={styles.sub}>across all stages</div>
      </div>
      <div className={`${styles.card} ${styles.yellow}`}>
        <div className={styles.label}>Interviews</div>
        <div className={styles.value}>{interviews}</div>
        <div className={styles.sub}>in progress</div>
      </div>
      <div className={`${styles.card} ${styles.green}`}>
        <div className={styles.label}>Offers</div>
        <div className={styles.value}>{offers}</div>
        <div className={styles.sub}>pending decision</div>
      </div>
      <div className={`${styles.card} ${styles.red}`}>
        <div className={styles.label}>Follow-ups Due</div>
        <div className={styles.value}>{followupsDue}</div>
        <div className={styles.sub}>action needed</div>
      </div>
    </div>
  );
}
