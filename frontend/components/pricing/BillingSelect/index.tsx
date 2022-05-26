
import { Button, Typography, Space } from 'antd';
import styles from './styles.module.css';
import type { BillingType } from '../../../types'


type Props = {
   type: BillingType;
   onClick: (event: React.MouseEvent<HTMLElement>, type: BillingType) => void;
}


const BillingSelect: React.FunctionComponent<Props> = (props) => {
   return (
      <section className={`text-center mx-auto ${styles.billingContainer}`}>
         <div className={`rounded-md p-1 ${styles.btnsWrp}`}>
            <Space>
               <Button 
                  shape={props.type === "month" ? "round" : "default"} 
                  onClick={event => props.onClick(event, "month")} 
                  className={`
                     ${styles.billingBtn} ${props.type === "month" ? styles.activeBilling : ''}
                  `}
               >
                  Monthly Billing
               </Button>
               <Button 
                  shape={props.type === "year" ? "round" : "default"} 
                  className={
                     `${styles.billingBtn} ${props.type === "year" ? styles.activeBilling : ''}
                  `}
                  onClick={event => props.onClick(event, "year")} 
               >
                  Yearly Billing
                  <Typography.Text 
                     type="secondary" 
                     className="text-xs" 
                     style={{ display: 'block' }}
                  >
                     2 months free
                  </Typography.Text>
               </Button>
            </Space>
         </div>
      </section>
   );
}

export default BillingSelect;
