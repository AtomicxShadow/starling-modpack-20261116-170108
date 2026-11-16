// SPDX-License-Identifier: GPL-3.0-or-later
// Starling 0.8.0 stores the prediction map inside BlockPredictions. Injected
// below that module, these methods can access it without exposing its fields.
impl super::BlockPredictions {
    /// An unsequenced server's update must reach the world immediately.
    pub fn viahorizon_forget_block(&mut self, pos: [i32; 3]) {
        self.verified.remove(&pos);
    }

    /// Forget acknowledged bookkeeping without restoring any saved block or
    /// player position. Later predictions and the sequence counter survive.
    pub fn viahorizon_forget_up_to(&mut self, sequence: i32) {
        self.verified.retain(|_, prediction| prediction.sequence > sequence);
    }
}

#[cfg(test)]
mod tests {
    use super::super::BlockPredictions;
    use horizon_core::geometry::Vec3;

    #[test]
    fn correction_releases_only_its_block_and_keeps_teleport_history() {
        let mut predictions = BlockPredictions::default();
        let sequence = predictions.start();
        let at = Some(Vec3::new(1.0, 64.0, 1.0));
        predictions.retain([1, 64, 1], 1, at, sequence);
        predictions.retain([2, 64, 1], 2, at, sequence);
        predictions.on_teleport();
        predictions.viahorizon_forget_block([1, 64, 1]);
        assert!(!predictions.update([1, 64, 1], 0));
        assert!(predictions.update([2, 64, 1], 3));
        let settled = predictions.end_up_to(sequence);
        assert_eq!(settled.len(), 1);
        assert_eq!(settled[0].pos, [2, 64, 1]);
        assert_eq!(settled[0].state, 3);
        assert_eq!(settled[0].player, None);
        assert_eq!(predictions.start(), sequence + 1);
    }

    #[test]
    fn synthetic_ack_forgets_only_actions_up_to_its_sequence() {
        let mut predictions = BlockPredictions::default();
        for x in 1..=3 {
            let sequence = predictions.start();
            predictions.retain([x, 64, 0], x, None, sequence);
        }
        predictions.viahorizon_forget_up_to(2);
        assert!(!predictions.update([1, 64, 0], 0));
        assert!(!predictions.update([2, 64, 0], 0));
        assert!(predictions.update([3, 64, 0], 4));
        assert!(predictions.end_up_to(2).is_empty());
        let settled = predictions.end_up_to(3);
        assert_eq!(settled.len(), 1);
        assert_eq!(settled[0].pos, [3, 64, 0]);
        assert_eq!(settled[0].state, 4);
        assert_eq!(predictions.start(), 4);
    }

    #[test]
    fn an_older_ack_keeps_a_block_predicted_again_by_a_later_action() {
        let mut predictions = BlockPredictions::default();
        let older = predictions.start();
        predictions.retain([1, 64, 0], 1, None, older);
        let later = predictions.start();
        predictions.retain([1, 64, 0], 2, None, later);
        predictions.viahorizon_forget_up_to(older);
        assert!(predictions.update([1, 64, 0], 3));
        predictions.viahorizon_forget_up_to(later);
        assert!(predictions.end_up_to(later).is_empty());
    }
}
