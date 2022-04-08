// import { Button } from 'antd'
import { Button } from '@chakra-ui/react'
import styles from './styles.module.css'
import { BsChevronDoubleDown } from 'react-icons/bs'


const CoverSection: React.FunctionComponent = () => {
  return (
      <section className={`flex items-center ${styles.container}`}>
         <div className={`ml-5 ${styles.sectionDiv}`}>
            <h1 className="mb-7">
               Copy & paste between multiple devices.
            </h1>
            <h2 className="mb-4">
               Easily copy, paste and transfer text and files from one device to another.
            </h2>
            <Button 
               size="lg" 
               variant="outline" 
               rightIcon={<BsChevronDoubleDown className={styles.downArrow} />}
               className={styles.ctaButton}
            >
               Continue
            </Button>
         </div>
      </section>
   );
}

export default CoverSection;
