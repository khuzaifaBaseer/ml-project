export type Feature = {
  name: string;
  label: string;
  kind: 'number' | 'category';
  required: boolean;
  options?: string[];
  min?: number;
  max?: number;
};

export const FEATURES: Feature[] = [
  { name: 'Protocol', label: 'Protocol', kind: 'number', required: true, min: 0 },
  { name: 'Tot_Bwd_Pkts', label: 'Total Backward Packets', kind: 'number', required: true, min: 0 },
  { name: 'Flow_Pkts/s', label: 'Flow Packets/s', kind: 'number', required: true, min: 0 },
  { name: 'Flow_IAT_Min', label: 'Flow IAT Min', kind: 'number', required: true, min: 0 },
  { name: 'Fwd_IAT_Mean', label: 'Forward IAT Mean', kind: 'number', required: true, min: 0 },
  { name: 'Fwd_Pkts/s', label: 'Forward Packets/s', kind: 'number', required: true, min: 0 },
  { name: 'SYN_Flag_Cnt', label: 'SYN Flag Count', kind: 'number', required: true, min: 0 },
  { name: 'RST_Flag_Cnt', label: 'RST Flag Count', kind: 'number', required: true, min: 0 },
  { name: 'URG_Flag_Cnt', label: 'URG Flag Count', kind: 'number', required: true, min: 0 },
  { name: 'ECE_Flag_Cnt', label: 'ECE Flag Count', kind: 'number', required: true, min: 0 },
  { name: 'Fwd_Seg_Size_Avg', label: 'Forward Segment Size Avg', kind: 'number', required: true, min: 0 },
  { name: 'Subflow_Fwd_Pkts', label: 'Subflow Forward Packets', kind: 'number', required: true, min: 0 },
  { name: 'Subflow_Bwd_Pkts', label: 'Subflow Backward Packets', kind: 'number', required: true, min: 0 },
  { name: 'Subflow_Bwd_Byts', label: 'Subflow Backward Bytes', kind: 'number', required: true, min: 0 },
  { name: 'Fwd_Act_Data_Pkts', label: 'Forward Active Data Packets', kind: 'number', required: true, min: 0 },
];