import com.sun.org.apache.xpath.internal.operations.Bool

class Car(private var weight: Double,private var size: Int){
    val isNew: Boolean
    get() {
        return weight > size
    }
}